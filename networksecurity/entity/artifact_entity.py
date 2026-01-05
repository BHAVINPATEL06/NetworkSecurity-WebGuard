from dataclasses import dataclass

@dataclass
## As the DataIngestionArtifact will give the output file path of the train and test files.
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
## As the DataValidationArtifact will give the output file path of the valid and invalid files along with the drift report file path.
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
## As the DataTransformationArtifact will give the output file path of the transformed object file along with the transformed train and test file paths.
class DataTransformationArtifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str
