# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml._common._error_definition import error_decorator
from azureml._common._error_definition.system_error import ClientError
from azureml._common._error_definition.user_error import (
    ArgumentBlankOrEmpty, ArgumentInvalid, ArgumentMismatch,
    ArgumentOutOfRange, Authentication, BadArgument, BadData, Conflict,
    ConnectionFailure, EmptyData, InvalidDimension, MalformedArgument, Memory,
    MissingData, NotFound, NotReady, NotSupported, ResourceExhausted, Timeout)
from azureml.automl.core.shared._diagnostics.error_strings import \
    AutoMLErrorStrings


# region ArgumentBlankOrEmpty
@error_decorator(use_parent_error_code=True)
class FeaturizationConfigEmptyFillValue(ArgumentBlankOrEmpty):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_EMPTY_FILL_VALUE


# endregion


# region ArgumentInvalid
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_TYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentWithSupportedValues(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_WITH_SUPPORTED_VALUES


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentWithSupportedValuesForTask(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_WITH_SUPPORTED_VALUES_FOR_TASK


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentForTask(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_FOR_TASK


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class TensorflowAlgosAllowedButDisabled(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TENSORFLOW_ALGOS_ALLOWED_BUT_DISABLED


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidCVSplits(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_CV_SPLITS


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidInputDatatype(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_INPUT_DATATYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InputDataWithMixedType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INPUT_DATA_WITH_MIXED_TYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class AllAlgorithmsAreBlocked(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_ALGORITHMS_ARE_BLOCKED


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidComputeTargetForDatabricks(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_COMPUTE_TARGET_FOR_DATABRICKS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class EmptyLagsForColumns(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.EMPTY_LAGS_FOR_COLUMNS


@error_decorator(use_parent_error_code=True)
class TimeseriesInvalidDateOffsetType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_INVALID_DATE_OFFSET_TYPE


class TimeseriesInvalidTimestamp(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_INVALID_TIMESTAMP


@error_decorator(use_parent_error_code=True)
class OnnxNotEnabled(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.ONNX_NOT_ENABLED


@error_decorator(use_parent_error_code=True)
class OnnxSplitsNotEnabled(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.ONNX_SPLITS_NOT_ENABLED


@error_decorator(use_parent_error_code=True)
class OnnxUnsupportedDatatype(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.ONNX_UNSUPPORTED_DATATYPE


@error_decorator(details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-auto-features")
class FeaturizationRequired(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.FEATURIZATION_REQUIRED


class FeatureTypeUnsupported(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.FEATURE_TYPE_UNSUPPORTED


# endregion


# region ArgumentMismatch
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class AllowedModelsSubsetOfBlockedModels(ArgumentMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALLOWED_MODELS_SUBSET_OF_BLOCKED_MODELS


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class ConflictingValueForArguments(ArgumentMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_VALUE_FOR_ARGUMENTS


@error_decorator(use_parent_error_code=True)
class InvalidDampingSettings(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_DAMPING_SETTINGS


@error_decorator(use_parent_error_code=True)
class ConflictingFeaturizationConfigDroppedColumns(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_FEATURIZATION_CONFIG_DROPPED_COLUMNS


@error_decorator(use_parent_error_code=True)
class ConflictingFeaturizationConfigReservedColumns(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_FEATURIZATION_CONFIG_RESERVED_COLUMNS


# endregion


# region BadArgument
@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidFeaturizer(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_FEATURIZER


@error_decorator(use_parent_error_code=True)
class InvalidSTLFeaturizerForMultiplicativeModel(InvalidFeaturizer):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_STL_FEATURIZER_FOR_MULTIPLICATIVE_MODEL


@error_decorator(use_parent_error_code=True)
class FeaturizationConfigParamOverridden(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_PARAM_OVERRIDDEN


@error_decorator(use_parent_error_code=True)
class FeaturizationConfigMultipleImputers(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_MULTIPLE_IMPUTERS


class MissingColumnsInData(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.MISSING_COLUMNS_IN_DATA


@error_decorator(use_parent_error_code=True)
class NonOverlappingColumnsInTrainValid(MissingColumnsInData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NON_OVERLAPPING_COLUMNS_IN_TRAIN_VALID


@error_decorator(use_parent_error_code=True)
class FeaturizationConfigColumnMissing(MissingColumnsInData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_COLUMN_MISSING


@error_decorator(use_parent_error_code=True)
class GrainContainsEmptyValues(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_NAN_GRAIN_VALUES


# endregion


# region ArgumentOutOfRange
@error_decorator(use_parent_error_code=True)
class NCrossValidationsExceedsTrainingRows(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.N_CROSS_VALIDATIONS_EXCEEDS_TRAINING_ROWS


@error_decorator(use_parent_error_code=True)
class ExperimentTimeoutForDataSize(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.EXPERIMENT_TIMEOUT_FOR_DATA_SIZE


@error_decorator(use_parent_error_code=True)
class QuantileRange(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.QUANTILE_RANGE


# endregion


# region MalformedArgument
class MalformedJsonString(MalformedArgument):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MALFORMED_JSON_STRING


# endregion


# region NotReady
class ComputeNotReady(NotReady):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.COMPUTE_NOT_READY


# endregion


# region NotFound
class MethodNotFound(NotFound):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.METHOD_NOT_FOUND


class DatastoreNotFound(NotFound):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASTORE_NOT_FOUND


class DataPathNotFound(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_PATH_NOT_FOUND


class MissingSecrets(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MISSING_SECRETS


@error_decorator(details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/"
                             "how-to-configure-auto-train#train-and-validation-data")
class MissingValidationConfig(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MISSING_VALIDATION_CONFIG


@error_decorator(use_parent_error_code=True)
class NoMetricsData(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.NO_METRICS_DATA


class ModelMissing(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MODEL_MISSING


# endregion


# region NotSupported
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class LargeDataAlgorithmsWithUnsupportedArguments(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.LARGE_DATA_ALGORITHMS_WITH_UNSUPPORTED_ARGUMENTS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class FeatureUnsupportedForIncompatibleArguments(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURE_UNSUPPORTED_FOR_INCOMPATIBLE_ARGUMENTS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class NonDnnTextFeaturizationUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NON_DNN_TEXT_FEATURIZATION_UNSUPPORTED


class InvalidOperationOnRunState(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_OPERATION_ON_RUN_STATE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class FeaturizationConfigForecastingStrategy(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_FORECASTING_STRATEGY


class RemoteInferenceUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.REMOTE_INFERENCE_UNSUPPORTED


# A package is either missing or has an incompatible version installed.
class IncompatibleOrMissingDependency(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INCOMPATIBLE_OR_MISSING_DEPENDENCY


@error_decorator(use_parent_error_code=True)
class NotebookGenMissingDependency(IncompatibleOrMissingDependency):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NOTEBOOK_GEN_MISSING_DEPENDENCY


@error_decorator(use_parent_error_code=True)
class LocalLegacyDependencyMissing(IncompatibleOrMissingDependency):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.LOCAL_LEGACY_DEPENDENCY_MISSING


@error_decorator(use_parent_error_code=True)
class DependencyWrongVersion(IncompatibleOrMissingDependency):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DEPENDENCY_WRONG_VERSION


@error_decorator(use_parent_error_code=True)
class LoadModelDependencyMissing(IncompatibleOrMissingDependency):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.LOAD_MODEL_DEPENDENCY_MISSING


@error_decorator(use_parent_error_code=True)
class ExplainabilityPackageMissing(IncompatibleOrMissingDependency):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.EXPLAINABILITY_PACKAGE_MISSING


# Snapshot is either larger than 300MB or exceeds max allowed files.
@error_decorator(use_parent_error_code=False, details_uri="http://aka.ms/aml-largefiles")
class SnapshotLimitExceeded(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.SNAPSHOT_LIMIT_EXCEED


@error_decorator(use_parent_error_code=True)
class ContinueRunUnsupportedForAdb(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONTINUE_RUN_UNSUPPORTED_FOR_ADB


@error_decorator(use_parent_error_code=True)
class ContinueRunUnsupportedForUntrackedRuns(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONTINUE_RUN_UNSUPPORTED_FOR_UNTRACKED_RUNS


@error_decorator(use_parent_error_code=True)
class CancelUnsupportedForLocalRuns(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CANCEL_UNSUPPORTED_FOR_LOCAL_RUNS


@error_decorator(use_parent_error_code=True)
class SampleWeightsUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.SAMPLE_WEIGHTS_UNSUPPORTED


@error_decorator(use_parent_error_code=True)
class ModelExplanationsUnsupportedForAlgorithm(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.MODEL_EXPLANATIONS_UNSUPPORTED_FOR_ALGORITHM
# endregion


# region MissingData
class InsufficientSampleSize(MissingData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.INSUFFICIENT_SAMPLE_SIZE


# endregion


# region InvalidDimension
class DataShapeMismatch(InvalidDimension):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATA_SHAPE_MISMATCH


@error_decorator(use_parent_error_code=True)
class DatasetsFeatureCountMismatch(DataShapeMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASETS_FEATURE_COUNT_MISMATCH


@error_decorator(use_parent_error_code=True)
class SampleCountMismatch(DataShapeMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.SAMPLE_COUNT_MISMATCH


@error_decorator(use_parent_error_code=True)
class StreamingInconsistentFeatures(DataShapeMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.STREAMING_INCONSISTENT_FEATURES


# endregion


# region BadData
class AllTargetsUnique(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_TARGETS_UNIQUE


class AllTargetsOverlapping(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_TARGETS_OVERLAPPING


@error_decorator(details_uri="https://aka.ms/datasetfromdelimitedfiles")
class InconsistentNumberOfSamples(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INCONSISTENT_NUMBER_OF_SAMPLES


class PandasDatetimeConversion(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.PANDAS_DATETIME_CONVERSION_ERROR


class TimeseriesColumnNamesOverlap(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_COLUMN_NAMES_OVERLAP


class TimeseriesTypeMismatchFullCV(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_TYPE_MISMATCH_FULL_CV


class MaxHorizonExceeded(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MAX_HORIZON_EXCEEDED


class TimeColumnValueOutOfRange(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIME_COLUMN_VALUE_OUT_OF_RANGE


@error_decorator(use_parent_error_code=True)
class TimeseriesCustomFeatureTypeConversion(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_CUSTOM_FEATURE_TYPE_CONVERSION


class TimeseriesDfContainsNaN(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_DF_CONTAINS_NAN


# Base class of timeseries dataframe type errors.
class TimeseriesDfWrongTypeError(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_WRONG_TYPE_ERROR


@error_decorator(use_parent_error_code=True)
class TimeseriesDfWrongTypeOfValueColumn(TimeseriesDfWrongTypeError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_WRONG_TYPE_OF_VALUE_COLUMN


@error_decorator(use_parent_error_code=True)
class TimeseriesDfWrongTypeOfTimeColumn(TimeseriesDfWrongTypeError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_WRONG_TYPE_OF_TIME_COLUMN


@error_decorator(use_parent_error_code=True)
class TimeseriesDfWrongTypeOfLevelValues(TimeseriesDfWrongTypeError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_WRONG_TYPE_OF_LEVEL_VALUES


@error_decorator(use_parent_error_code=True)
class TimeseriesDfUnsupportedTypeOfLevel(TimeseriesDfWrongTypeError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_UNSUPPORTED_TYPE_OF_LEVEL


# Base class of timeseries dataframe frequency errors.
class TimeseriesDfFrequencyError(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_FREQUENCY_ERROR


@error_decorator(use_parent_error_code=True)
class TimeseriesDfFrequencyGenericError(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_FREQUENCY_GENERIC_ERROR


class TimeseriesDfFrequencyNotConsistent(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_FREQUENCY_NOT_CONSISTENT


@error_decorator(use_parent_error_code=True)
class TimeseriesDfMultiFrequenciesDiff(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_MULTI_FREQUENCIES_DIFF


@error_decorator(use_parent_error_code=True)
class TimeseriesDfCannotInferFrequencyFromTSId(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_CANNOT_INFER_FREQ_FROM_TS_ID


@error_decorator(use_parent_error_code=True)
class TimeseriesCannotInferFrequencyFromTimeIdx(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_CANNOT_INFER_FREQ_FROM_TIME_IDX


@error_decorator(use_parent_error_code=True)
class TimeseriesCannotInferSingleFrequencyForAllTS(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_CANNOT_INFER_SINGLE_FREQ_FOR_ALL_TS


class TimeseriesFrequencyNotSupported(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_FREQUENCY_NOT_SUPPORTED


class TimeseriesReferenceDatesMisaligned(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_REFERENCE_DATES_MISALIGNED


class TimeseriesTimeIndexDatesMisaligned(TimeseriesDfFrequencyError):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_TIME_IDX_DATES_MISALIGNED


class TimeseriesDfIncorrectFormat(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_INCORRECT_FORMAT


@error_decorator(use_parent_error_code=True)
class TimeseriesDfColValueNotEqualAcrossOrigin(TimeseriesDfIncorrectFormat):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_COL_VALUE_NOT_EQUAL_ACROSS_ORIGIN


@error_decorator(use_parent_error_code=True)
class TimeseriesDfIndexValuesNotMatch(TimeseriesDfIncorrectFormat):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_DF_INDEX_VALUES_NOT_MATCH


class TimeseriesNoDataContext(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_NO_DATA_CONTEXT


class TimeseriesNothingToPredict(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_NOTHING_TO_PREDICT


class TimeseriesNonContiguousTargetColumn(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_NON_CONTIGUOUS_TARGET_COLUMN


class TimeseriesMissingValuesInY(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_MISSING_VALUES_IN_Y


class TimeSeriesReservedColumn(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_RESERVED_COLUMN


class TransformerYMinGreater(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TRANSFORMER_Y_MIN_GREATER


class TooManyLabels(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TOO_MANY_LABELS


class BadDataInWeightColumn(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.BAD_DATA_IN_WEIGHT_COLUMN


class UnhashableValueInColumn(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.UNHASHABLE_VALUE_IN_COLUMN


@error_decorator(use_parent_error_code=True)
class DatasetContainsInf(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATASET_CONTAINS_INF


@error_decorator(use_parent_error_code=True)
class IndistinctLabelColumn(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.INDISTINCT_LABEL_COLUMN


@error_decorator(use_parent_error_code=True)
class InconsistentColumnTypeInTrainValid(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.INCONSISTENT_COLUMN_TYPE_IN_TRAIN_VALID


@error_decorator(use_parent_error_code=True)
class InvalidOnnxData(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.INVALID_ONNX_DATA


class AllFeaturesAreExcluded(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.ALL_FEATURES_ARE_EXCLUDED


class UnrecognizedFeatures(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.UNRECOGNIZED_FEATURES


@error_decorator(use_parent_error_code=True)
class TimeseriesEmptySeries(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_EMPTY_SERIES


@error_decorator(use_parent_error_code=True)
class DuplicateColumns(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DUPLICATE_COLUMNS


@error_decorator(use_parent_error_code=True,
                 details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cross-"
                             "validation-data-splits#specify-custom-cross-validation-data-folds")
class InvalidValuesInCVSplitColumn(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.INVALID_VALUES_IN_CV_SPLIT_COLUMN


class NoFeatureTransformationsAdded(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NO_FEATURE_TRANSFORMATIONS_ADDED


@error_decorator(use_parent_error_code=True)
class PowerTransformerInverseTransform(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.POWER_TRANSFORMER_INVERSE_TRANSFORM


class ContentModified(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONTENT_MODIFIED


class DataprepValidation(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATAPREP_VALIDATION


class DatabaseQuery(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATABASE_QUERY
# endregion


# region MissingData
@error_decorator(use_parent_error_code=True)
class GrainShorterThanTestSize(MissingData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.GRAIN_SHORTER_THAN_TEST_SIZE


@error_decorator(use_parent_error_code=True)
class GrainAbsent(MissingData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.GRAIN_ABSENT
# endregion


# region EmptyData
@error_decorator(use_parent_error_code=True)
class InputDatasetEmpty(EmptyData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.INPUT_DATASET_EMPTY


# endregion


# region Authentication
class DataPathInaccessible(Authentication):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_PATH_INACCESSIBLE


@error_decorator(use_parent_error_code=True,
                 details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-access-data#"
                             "supported-data-storage-service-types")
class MissingCredentialsForWorkspaceBlobStore(Authentication):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MISSING_CREDENTIALS_FOR_WORKSPACE_BLOB_STORE
# endregion


# region Conflict
class CacheOperation(Conflict):
    @property
    def message_format(self):
        return AutoMLErrorStrings.CACHE_OPERATION


@error_decorator(use_parent_error_code=True, is_transient=True)
class MissingCacheContents(CacheOperation):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MISSING_CACHE_CONTENTS
# endregion


# region ClientError
@error_decorator(details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/"
                             "resource-known-issues#automated-machine-learning")
class AutoMLInternal(ClientError):
    """Base class for all AutoML system errors."""

    @property
    def message_format(self):
        return AutoMLErrorStrings.AUTOML_INTERNAL


class Data(AutoMLInternal):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA


class Service(AutoMLInternal):
    @property
    def message_format(self):
        return AutoMLErrorStrings.SERVICE


# endregion


# region ResourceExhausted
class DiskFull(ResourceExhausted):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DISK_FULL
# endregion


# region Memory
class Memorylimit(Memory):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_MEMORY_ERROR


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/azurevmsizes")
class InsufficientMemory(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INSUFFICIENT_MEMORY


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/azurevmsizes")
class InsufficientMemoryWithHeuristics(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INSUFFICIENT_MEMORY_WITH_HEURISTICS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/azurevmsizes")
class InsufficientMemoryLikely(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INSUFFICIENT_MEMORY_LIKELY


# endregion


# region Timeout
@error_decorator(is_transient=True, details_uri="https://aka.ms/storageoptimization")
class DatasetFileRead(Timeout):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASET_FILE_READ


# endregion


# region ConnectionFailure
@error_decorator(use_parent_error_code=True, is_transient=True)
class HttpConnectionFailure(ConnectionFailure):
    @property
    def message_format(self):
        return AutoMLErrorStrings.HTTP_CONNECTION_FAILURE
# endregion
