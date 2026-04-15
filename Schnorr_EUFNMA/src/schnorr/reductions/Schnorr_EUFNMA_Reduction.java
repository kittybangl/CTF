package schnorr.reductions;

import java.math.BigInteger;
import java.util.HashMap;
import java.math.*;
import java.util.Random;
import genericGroups.GroupElement;
import genericGroups.IGroupElement;
import dlog.DLog_Challenge;
import dlog.I_DLog_Challenger;

import schnorr.I_Schnorr_EUFNMA_Adversary;
import schnorr.SchnorrSolution;
import schnorr.Schnorr_PK;
import utils.Pair;
import schnorr.I_Schnorr_EUF_Challenger;

import genericGroups.IBasicGroupElement;
public class Schnorr_EUFNMA_Reduction extends A_Schnorr_EUFNMA_Reduction{
    private DLog_Challenge challenge;
    private IGroupElement x;
    private IGroupElement gen;
    Schnorr_PK<IGroupElement> pk;
    HashMap<Pair<String, IGroupElement>, BigInteger> Sites = new HashMap<>();
    //final I_Schnorr_EUF_Challenger a;
    public Schnorr_EUFNMA_Reduction(I_Schnorr_EUFNMA_Adversary<IGroupElement, BigInteger> adversary) {
        super(adversary);
        //Do not change this constructor!
    }

    @Override
    public Schnorr_PK<IGroupElement> getChallenge() {
        //Write your Code here!
        /**
         * the public key as a group element
         */
        //public IGroupElement key;
        /**
         * the group generator
         */
        //public IGroupElement base;
        IGroupElement base = this.gen;
        IGroupElement key = this.x;
        Schnorr_PK<IGroupElement> ans = new Schnorr_PK<IGroupElement>(base, key);
        return ans;
    }

    @Override
    public BigInteger hash(String message, IGroupElement r) {
        //Write your Code here!
        // r.getGroupOrder();
        Pair<String, IGroupElement> tmp = new Pair<String,IGroupElement>(message, r);
        BigInteger p = r.getGroupOrder();

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
    BigInteger fastPow(BigInteger a, BigInteger k, BigInteger p){  // a 底数， k 指数， 求 a^k mod p
        BigInteger res = BigInteger.ONE;
        while(k.compareTo(BigInteger.ZERO) > 0){
            if (k.mod(BigInteger.TWO).equals(BigInteger.ONE)) 
                res = res.multiply(a).mod(p);
            a = a.multiply(a).mod(p);
            k = k.shiftRight(1);
        }
        return res;
    }
    BigInteger fractionMod(BigInteger a, BigInteger b, BigInteger p){  // a/b mod p
        return (a.mod(p).multiply(fastPow(b, p.subtract(BigInteger.TWO), p))).mod(p);
    }
    @Override
    public BigInteger run(I_DLog_Challenger<IGroupElement> challenger) {
        //Write your Code here!
        // DLog_Challenge challenge = challenger.getChallenge();
        // DLog_Challenge a = challenger.getChallenge();
        // // System.out.println(a);
        // I_Schnorr_EUF_Adversary.reset();
        // You can use the Triple class...
        this.challenge = challenger.getChallenge();
        this.x = (IGroupElement)challenge.x;
        this.gen = (IGroupElement)challenge.generator;
        Random randNum = new Random();
        int seed = randNum.nextInt(100000000);
        adversary.reset(seed);
        SchnorrSolution ans1 = adversary.run(this);
        //adversary.reset(seed);
        Sites.clear();
        adversary.reset(seed);
        SchnorrSolution ans2 = adversary.run(this);
        //IGroupElement a = challenge.generator;
        BigInteger p = x.getGroupOrder();
        BigInteger c1 = (BigInteger)ans1.signature.c;
        BigInteger c2 = (BigInteger)ans2.signature.c;
        BigInteger s1 = (BigInteger)ans1.signature.s;
        BigInteger s2 = (BigInteger)ans2.signature.s;
        BigInteger new_c = c1.subtract(c2);
        BigInteger new_s = s1.subtract(s2);
        if(c1.compareTo(c2) > 0){
            new_c = c1.subtract(c2);
            new_s = s1.subtract(s2);
        } else {
            new_c = c2.subtract(c1);
            new_s = s2.subtract(s1);
        }
        return fractionMod(new_s, new_c, p);
    }
    
}
