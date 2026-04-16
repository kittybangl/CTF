package katzwang.reductions;

import java.math.BigInteger;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

import ddh.DDH_Challenge;
import ddh.I_DDH_Challenger;
import genericGroups.IGroupElement;
import katzwang.A_KatzWang_EUFCMA_Adversary;
import katzwang.KatzWangPK;
import katzwang.KatzWangSignature;
import katzwang.KatzWangSolution;
import utils.NumberUtils;
import utils.Triple;
import utils.Pair;

public class KatzWang_EUFCMA_Reduction extends A_KatzWang_EUFCMA_Reduction {
    private DDH_Challenge<IGroupElement> challenge;
    private IGroupElement g;
    private IGroupElement gx;
    private IGroupElement gy;
    private IGroupElement gxy;
    // HashMap<Triple<String, IGroupElement, IGroupElement>, BigInteger> Sites = new HashMap<>();
    HashMap<String, BigInteger> Sites = new HashMap<>();
    
    public KatzWang_EUFCMA_Reduction(A_KatzWang_EUFCMA_Adversary adversary) {
        super(adversary);
        // Do not change this constructor
    }

    @Override
    public Boolean run(I_DDH_Challenger<IGroupElement, BigInteger> challenger) {
        // Implement your code here!
        var triple = new Triple<Integer, Integer, Integer>(1, 2, 3);
        this.challenge = challenger.getChallenge();
        this.g = this.challenge.generator;
        this.gx = this.challenge.x;
        this.gy = this.challenge.y;
        this.gxy = this.challenge.z;
        var a = adversary.run(this);
        if (a == null) {
            return false;
        } else {
            return true;
        }
    }

    @Override
    public KatzWangPK<IGroupElement> getChallenge() {
        // Implement your code here!
        KatzWangPK<IGroupElement> ans = new KatzWangPK<IGroupElement>(this.g, this.gy, this.gx, this.gxy);
        //KatzWangSolution<BigInteger> katzwang.A_KatzWang_EUFNMA_Adversary.run(I_KatzWang_EUFNMA_Challenger<IGroupElement, BigInteger> arg0)
        
        return ans;
    }

    @Override
    public BigInteger hash(IGroupElement comm1, IGroupElement comm2, String message) {
        // Implement your code here!
        // Triple<String, IGroupElement, IGroupElement> tmp = new Triple<String, IGroupElement, IGroupElement>(message, comm1, comm2);
        BigInteger p = comm1.getGroupOrder();

        if(Sites.containsKey(message)){
            return Sites.get(message);
        }
        Random rand = new Random();
        BigInteger res = new BigInteger(p.bitLength(), rand);
        while( res.compareTo(p) >= 0 ) {
            res = new BigInteger(p.bitLength(), rand);
        }
        Sites.put(message, res);
        return res;
    }

    @Override
    public KatzWangSignature<BigInteger> sign(String message) {
        // Implement your code here!
        BigInteger p = gx.getGroupOrder();
        Random rand = new Random();
        BigInteger c = new BigInteger(p.bitLength(), rand);
        while( c.compareTo(p) >= 0 ) {
            c = new BigInteger(p.bitLength(), rand);
        }
        BigInteger s = new BigInteger(p.bitLength(), rand);
        while( s.compareTo(p) >= 0 ) {
            s = new BigInteger(p.bitLength(), rand);
        }
        Sites.put(message, c);
        BigInteger minus_c = c.multiply(BigInteger.ONE.negate()); 
        IGroupElement R = this.g.power(s).multiply(this.gx.power(minus_c));
        // BigInteger tmp = hash(message, R);
        // Sites.put(new Triple<String,IGroupElement, IGroupElement>(message, gx, gxy), c);
        return new KatzWangSignature<BigInteger>(c, s);
    }
}
