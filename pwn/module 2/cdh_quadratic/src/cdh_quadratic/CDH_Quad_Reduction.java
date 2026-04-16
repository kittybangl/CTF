package cdh_quadratic;

import java.math.BigInteger;
import cdh.CDH_Challenge;
import cdh.I_CDH_Challenger;
import genericGroups.IGroupElement;

/**
 * This is the file you need to implement.
 * 
 * Implement the methods {@code run} and {@code getChallenge} of this class.
 * Do not change the constructor of this class.
 */
public class CDH_Quad_Reduction extends A_CDH_Quad_Reduction<IGroupElement> {

    private I_CDH_Challenger<IGroupElement> challenger;
    private IGroupElement generator;
    private IGroupElement x;
    private IGroupElement y;
    private CDH_Challenge<IGroupElement> challenge;
    /**
     * Do NOT change or remove this constructor. When your reduction can not provide
     * a working standard constructor, the TestRunner will not be able to test your
     * code and you will get zero points.
     */
    public CDH_Quad_Reduction() {
        // Do not add any code here!
    }


    IGroupElement f1(IGroupElement g, IGroupElement gX, IGroupElement gY) {
        this.generator = g;
        this.x = gX;
        this.y = gY;
        IGroupElement ans = adversary.run(this);
        return ans;
    }

    IGroupElement f2(IGroupElement g, IGroupElement gX, IGroupElement gY) {
        IGroupElement abcd = f1(g, gX, gY);
        IGroupElement d = f1(g, g.power(BigInteger.ZERO), g.power(BigInteger.ZERO));
        return abcd.multiply(d.invert());
    }

    IGroupElement f3(IGroupElement g, IGroupElement gX, IGroupElement gY) {
        IGroupElement abcd = f1(g, gX, gY);
        IGroupElement cd = f1(g, g.power(BigInteger.ZERO), gY);
        return abcd.multiply(cd.invert());
    }

    IGroupElement f4(IGroupElement g, IGroupElement gX, IGroupElement gY) {
        IGroupElement abcd = f1(g, gX, gY);
        IGroupElement abc = f2(g, gX, gY);
        IGroupElement ab = f3(g, gX, gY);
        IGroupElement bd = f1(g, gX, g.power(BigInteger.ZERO));
        IGroupElement cd = f1(g, g.power(BigInteger.ZERO), gY);
        IGroupElement d = abcd.multiply(abc.invert());
        IGroupElement c = abc.multiply(ab.invert());
        IGroupElement b = bd.multiply(d.invert());
        // IGroupElement tmp1 = abcd.multiply(cd.invert()).multiply(b.invert());
        // IGroupElement tmp2 = abcd.multiply(d.invert()).multiply(c.invert()).multiply(b.invert());
        // System.out.println(tmp1.equals(tmp2));
        return abcd.multiply(d.invert()).multiply(c.invert()).multiply(b.invert());
        // return abcd.multiply(d.invert()).multiply(c.invert());
    }
    @Override
    public IGroupElement run(I_CDH_Challenger<IGroupElement> challenger) {
        // This is one of the both methods you need to implement.
        CDH_Challenge challenge = challenger.getChallenge();
        // By the following call you will receive a DLog challenge.
        this.generator = (IGroupElement)challenge.generator;
        this.x = (IGroupElement)challenge.x;
        this.y = (IGroupElement)challenge.y;
        CDH_Challenge<IGroupElement> cdh_challenge = new CDH_Challenge<IGroupElement>(this.generator, this.x, this.y);
        IGroupElement ga = f4(this.generator, this.generator, this.generator);
        BigInteger p = this.generator.getGroupOrder();
        p = p.subtract(BigInteger.valueOf(3));
        boolean[] isOdd = new boolean[1000];
        int i = 0;
        IGroupElement ans = ga;
        // IGroupElement tmp1 = f3(this.generator, ans, ga.power(BigInteger.ZERO));
        // IGroupElement tmp2 = f3(this.generator, ga.power(BigInteger.ZERO), ans);
        // System.out.println(tmp1.equals(tmp2));
        // p = BigInteger.valueOf(12);
        while (p.compareTo(BigInteger.ONE) > 0) {
            isOdd[i] = p.testBit(0);
            if(isOdd[i]) {
                p = p.divide(BigInteger.TWO);
            } else {
                p = p.subtract(BigInteger.ONE);
            }
            i++;
        }

        for(int j = i - 1; j >= 0; j--) {
            if(isOdd[j]) {
                ans = f4(this.generator, ans, ans);
            } else {
                ans = f4(this.generator, ans, this.generator);
            }
        }
        // your reduction does not need to be tight. I.e., you may call
        // adversary.run(this) multiple times.

        // Remember that this is a group of prime order p.
        // In particular, we have a^(p-1) = 1 mod p for each a != 0.
        // ans = f4(this.generator, ans, ga);
        // System.out.println(ans.equals(ga));
        return f4(this.generator, ans, f4(cdh_challenge.generator, cdh_challenge.x, cdh_challenge.y));
    }

    @Override
    public CDH_Challenge<IGroupElement> getChallenge() {

        // This is the second method you need to implement.
        // You need to create a CDH challenge here which will be given to your CDH
        // adversary.
        IGroupElement generator = this.generator;
        IGroupElement x = this.x;
        IGroupElement y = this.y;
        // Instead of null, your cdh challenge should consist of meaningful group
        // elements.
        CDH_Challenge<IGroupElement> cdh_challenge = new CDH_Challenge<IGroupElement>(generator, x, y);

        return cdh_challenge;
    }
}
