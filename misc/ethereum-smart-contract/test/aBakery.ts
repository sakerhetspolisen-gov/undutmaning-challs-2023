import { time, loadFixture } from "@nomicfoundation/hardhat-network-helpers";
import { anyValue } from "@nomicfoundation/hardhat-chai-matchers/withArgs";
import { expect } from "chai";
import { ethers } from "hardhat";

describe("ABakery", function () {
  // We define a fixture to reuse the same setup in every test.
  // We use loadFixture to run this setup once, snapshot that state,
  // and reset Hardhat Network to that snapshot in every test.
  async function deployABakery() {

    // Contracts are deployed using the first signer/account by default
    const [owner, feeCollector, operator ] = await ethers.getSigners();

    const ABakery = await ethers.getContractFactory("ABakery");
    const aBakery = await ABakery.deploy();

    return { aBakery, owner, feeCollector, operator };
  }

  // describe("Deployment", function () {
  //   it("Should set the right owner", async function () {
  //     const { aBakery, owner } = await loadFixture(deployABakery);
  //     expect(await aBakery.owner()).to.equal(owner.address);
  //   });
  // });
  // describe("Deployment", function () {
  //   it("Should set the right owner", async function () {
  //     const { aBakery, owner } = await loadFixture(deployABakery);
  //     expect(await aBakery.owner()).to.equal(owner.address);
  //   });
  // });

  describe("AddFlavor", function () {
    it("Should not accept other then owner to set flavor", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      await expect(aBakery.connect(feeCollector).addFlavor(0, 'Bla bla bla')).to.be.revertedWith(
        "Only the owner can add a new pastry flavor."
      );  
    });

    it("Should not accept add more than 64 flavors", async function () {
      const { aBakery } = await loadFixture(deployABakery);
      await expect(aBakery.addFlavor(8, 'Bla bla bla')).to.be.revertedWith(
        "To many flavors for the baker to handle."
      );  
    });

    it("Should accept owner to add flavor", async function () {
      const { aBakery } = await loadFixture(deployABakery);
      await aBakery.addFlavor(0, 'Bla bla bla');
    });
  });

   describe("GetFlavors", function () {
    it("Should accept all to get the flavor of the day", async function () {
      const { aBakery } = await loadFixture(deployABakery);
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      expect(await aBakery.getFlavors()).to.equal('Bla bla bla');
    });
  });


  describe("SetPastry", function () {
    it("Should not accept other then owner to set pastry of the day", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      await expect(aBakery.connect(feeCollector).setPastry('stårta')).to.be.revertedWith(
        "Only the owner can set the pastry of the day."
      );  
    });

    it("Should accept owner to set pastry of the day", async function () {
      const { aBakery } = await loadFixture(deployABakery);
      await aBakery.setPastry('tårta');
    });
  });


  describe("OrderPastry", function () {
    it("Should not accept order for unsupported flavor", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      await aBakery.setPastry('tårta');
      await expect(aBakery.orderPastry('Bla bla bla')).to.be.revertedWith(
        "Sorry, we don't have that flavor."
      );
    });

    it("Should not accept order for unsupported flavor (spelling)", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      await aBakery.setPastry('tårta');
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      await expect(aBakery.orderPastry('Lingon')).to.be.revertedWith(
        "Sorry, we don't have that flavor."
      );
    });

    it("Should accept order for a second flavor", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      await aBakery.setPastry('tårta');
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      await aBakery.addFlavor(2, 'blåbär');
      await expect(aBakery.orderPastry('blåbär')).to.be.revertedWith(
        "A pastry cost 10000 gwei GoerliETH."
      );
    });

    it("Should not accept order with to wrong amount", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      const fee = ethers.utils.parseEther("0.00002");
      await aBakery.setPastry('tårta');
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      await expect(aBakery.connect(feeCollector).orderPastry('lingon', {value: fee})).to.be.revertedWith(
        "A pastry cost 10000 gwei GoerliETH."
      );
    });

    it("Should accept order with right amount and accepted flavor", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      const fee = ethers.utils.parseEther("0.00001");
      await aBakery.setPastry('tårta');
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      await aBakery.connect(feeCollector).orderPastry('lingon', {value: fee});
    });
  });

  describe("PickupOrderedPastry", function () {
    it("Should not accept unordered requestes", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      await expect(aBakery.pickupOrderedPastry()).to.be.revertedWith(
        "You haven't ordered any pastry (yet)."
      );
    });

    it("Should not accept request of order for other then customer", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      const fee = ethers.utils.parseEther("0.00001");
      await aBakery.setPastry('tårta');
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      await aBakery.orderPastry('lingon', {value: fee});
      await expect(aBakery.connect(feeCollector).pickupOrderedPastry()).to.be.revertedWith(
        "You haven't ordered any pastry (yet)."
      );
    });

    it("Should return order for right customer", async function () {
      const { aBakery, owner, feeCollector } = await loadFixture(deployABakery);
      const fee = ethers.utils.parseEther("0.00001");
      await aBakery.setPastry('tårta');
      await aBakery.addFlavor(0, 'Bla bla bla');
      await aBakery.addFlavor(1, 'lingon');
      await aBakery.connect(feeCollector).orderPastry('lingon', {value: fee});
      expect(await aBakery.connect(feeCollector).pickupOrderedPastry()).to.equal('tårta');
    });
  });
});