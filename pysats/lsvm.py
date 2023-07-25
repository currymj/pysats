from jnius import MetaJavaClass, JavaMethod
from .simple_model import SimpleModel


class _Lsvm(SimpleModel, metaclass=MetaJavaClass):
    # We have to define the java class and any method we're going to use in this child class
    __javaclass__ = "org/spectrumauctions/sats/core/model/lsvm/LocalSynergyValueModel"
    setNumberOfNationalBidders = JavaMethod("(I)V")
    setNumberOfRegionalBidders = JavaMethod("(I)V")
    createWorld = JavaMethod(
        "(Lorg/spectrumauctions/sats/core/util/random/RNGSupplier;)Lorg/spectrumauctions/sats/core/model/lsvm/LSVMWorld;"
    )
    createPopulation = JavaMethod(
        "(Lorg/spectrumauctions/sats/core/model/World;Lorg/spectrumauctions/sats/core/util/random/RNGSupplier;)Ljava/util/List;"
    )
    setLegacyLSVM = JavaMethod("(Z)V")
    setNumberOfColumnsInterval = JavaMethod("(I)V")

    def __init__(
        self,
        seed,
        number_of_national_bidders,
        number_of_regional_bidders,
        isLegacyLSVM=False,
        store_files=False,
        number_of_columns=None
    ):
        self.number_of_national_bidders = number_of_national_bidders
        self.number_of_regional_bidders = number_of_regional_bidders
        self.isLegacy = isLegacyLSVM
        self.number_of_columns = number_of_columns
        super().__init__(
            seed=seed,
            mip_path="org.spectrumauctions.sats.opt.model.lsvm.LSVMStandardMIP",
            store_files=store_files,
        )

    def prepare_world(self):
        self.setNumberOfNationalBidders(self.number_of_national_bidders)
        self.setNumberOfRegionalBidders(self.number_of_regional_bidders)
        self.setLegacyLSVM(self.isLegacy)
        if self.number_of_columns is not None:
            self.setNumberOfColumnsInterval(self.number_of_columns)

    def get_model_name(self):
        return "LSVM"
