import unittest
from pysats import PySats


class LsvmTest(unittest.TestCase):
    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_lsvm(self):
        instance_seed = 2
        lsvm = self.pysats.create_lsvm(seed=instance_seed, isLegacyLSVM=False)
        print("\n\nMAIN LSVM TEST  | Seed:", instance_seed)
        bidder_ids = list(lsvm.get_bidder_ids())
        print("Bidder IDs: {}".format(bidder_ids))
        print("Good IDs: {}".format(lsvm.get_good_ids()))
        for bidder_id in bidder_ids:
            print("\nBidder {}".format(bidder_id))
            print(
                "Query value for bundle [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1]"
            )
            value = lsvm.calculate_value(
                bidder_id, [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1]
            )
            print(f"value={value}")
            print("Multiple bundles at once:")
            values = lsvm.calculate_values(
                bidder_id,
                [
                    [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
                ],
            )
            print(f"values={values}")
            print("Generate 3 uniform random bids")
            bids = lsvm.get_uniform_random_bids(bidder_id, 3)
            for bid in bids:
                print(bid)

        print("\nCalculate efficient allocation: goods | value")
        allocation, total_value = lsvm.get_efficient_allocation()
        for k, v in allocation.items():
            tmp = f"Bidder_{k}: "
            goods = v["good_ids"]
            value = v["value"]
            tmp += f"{goods} | {value}"
            print(tmp)
        self.assertEqual(allocation[bidder_ids[0]]["value"], 10.899624216435544)
        self.assertEqual(allocation[bidder_ids[1]]["value"], 14.863588882700238)
        self.assertEqual(allocation[bidder_ids[2]]["value"], 197.91229024726067)
        self.assertEqual(allocation[bidder_ids[3]]["value"], 0.0)
        self.assertEqual(allocation[bidder_ids[4]]["value"], 16.870979861919466)
        self.assertEqual(allocation[bidder_ids[5]]["value"], 209.7691468662042)

    def test_lsvm_bid_seeds(self):
        instance_seed = 22
        lsvm = self.pysats.create_lsvm(seed=instance_seed, isLegacyLSVM=False)
        print("\n\nTEST LSVM random bid generators | Seed:", instance_seed)
        bidder_ids = lsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = lsvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = lsvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)
            # Generate some bids with the new method
            bids = lsvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            new_bids = lsvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

    def test_multi_instance(self):
        instance_seed = 3
        lsvm = self.pysats.create_lsvm(seed=instance_seed, isLegacyLSVM=False)
        print("\n\nTEST LSVM multi instance generation | Seed:", instance_seed)
        bidder_ids = lsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print("Bidder: ", bidder_id)
        self.assertEqual(len(bidder_ids), 6)
    
    def test_lsvm_numitems(self):
        instance_seed = 3
        lsvm = self.pysats.create_lsvm(seed=instance_seed, number_of_national_bidders=1, number_of_regional_bidders=1, isLegacyLSVM=False, number_of_columns=2)
        print("\n\nTEST LSVM num items | Seed:", instance_seed)
        bidder_ids = lsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print("Bidder: ", bidder_id)
        self.assertEqual(len(bidder_ids), 2)
        self.assertEqual(len(lsvm.get_good_ids()), 6)

    def test_goods_of_interest(self):
        instance_seed = 4
        lsvm = self.pysats.create_lsvm(seed=instance_seed, isLegacyLSVM=False)
        print("\n\nTEST LSVM goods of interest per bidder | Seed:", instance_seed)
        for bidder_id in lsvm.get_bidder_ids():
            goods_of_interest = lsvm.get_goods_of_interest(bidder_id)
            print(f"Bidder_{bidder_id}: {goods_of_interest}")

    def test_demand_query(self):
        instance_seed = 333
        lsvm = self.pysats.create_lsvm(seed=instance_seed, isLegacyLSVM=False)
        price_vector = [0.0] * len(lsvm.get_good_ids())
        for bidder_id in lsvm.get_bidder_ids():
            demanded_bundles = lsvm.get_best_bundles(bidder_id, price_vector, 3)
            first = demanded_bundles[0]
            for bundle in demanded_bundles[1:]:
                self.assertNotEqual(first, bundle)
                self.assertLessEqual(
                    lsvm.calculate_value(bidder_id, bundle),
                    lsvm.calculate_value(bidder_id, first),
                )
        price_vector = [1e7] * len(lsvm.get_good_ids())
        for bidder_id in lsvm.get_bidder_ids():
            demanded_bundles = lsvm.get_best_bundles(bidder_id, price_vector, 3)
            self.assertEqual(len(demanded_bundles), 1)
            for value in demanded_bundles[0]:
                self.assertEqual(value, 0)


if __name__ == "__main__":
    unittest.main()
