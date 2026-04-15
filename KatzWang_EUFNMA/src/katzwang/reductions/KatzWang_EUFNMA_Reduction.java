package katzwang.reductions;
import java.util.HashMap;
import java.math.BigInteger;
import ddh.DDH_Challenge;
import ddh.I_DDH_Challenger;
import genericGroups.IGroupElement;
import katzwang.A_KatzWang_EUFNMA_Adversary;
import katzwang.KatzWangPK;
import utils.Triple;

import java.util.Random;
public class KatzWang_EUFNMA_Reduction extends A_KatzWang_EUFNMA_Reduction {
    private DDH_Challenge<IGroupElement> challenge;
    private IGroupElement g;
    private IGroupElement gx;
    private IGroupElement gy;
    private IGroupElement gxy;
    //I_DDH_Challenger<IGroupElement, BigInteger> challenger;
    HashMap<Triple<String, IGroupElement, IGroupElement>, BigInteger> Sites = new HashMap<>();
    public KatzWang_EUFNMA_Reduction(A_KatzWang_EUFNMA_Adversary adversary) {
        super(adversary);
        // Do not change this constructor!
    }

    @Override
    public Boolean run(I_DDH_Challenger<IGroupElement, BigInteger> challenger) {
        // Write your Code here!

        // You can use the Triple class...
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
        // Write your Code here!
        KatzWangPK<IGroupElement> ans = new KatzWangPK<IGroupElement>(this.g, this.gy, this.gx, this.gxy);
        //KatzWangSolution<BigInteger> katzwang.A_KatzWang_EUFNMA_Adversary.run(I_KatzWang_EUFNMA_Challenger<IGroupElement, BigInteger> arg0)
        
        return ans;
    }

    @Override
    public BigInteger hash(IGroupElement comm1, IGroupElement comm2, String message) {
        // Write your Code here!
        Triple<String, IGroupElement, IGroupElement> tmp = new Triple<String, IGroupElement, IGroupElement>(message, comm1, comm2);
        BigInteger p = comm1.getGroupOrder();

        if(Sites.containsKey(tmp)){
            return Sites.get(tmp);
        }
        Random rand = new Random();
        BigInteger res = new BigInteger(p.bitLength(), rand);
        while( res.compareTo(p) >= 0 ) {
            res = new BigInteger(p.bitLength(), rand);
        }
        Sites.put(tmp, res);
        return res;
    }

}
