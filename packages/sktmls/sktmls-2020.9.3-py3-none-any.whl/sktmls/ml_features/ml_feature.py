from dateutil import parser
from enum import Enum

from sktmls import MLSClient, MLSENV, MLSRuntimeENV


class MLFeature:
    class Type(Enum):
        """
        AutoML 피쳐 타입입니다.

        - SCORE: 스코어 기반 고객 타겟팅
        - CLASSIFICATION: 분류
        - REGRESSION: 회귀
        """

        CATEGORY = "category"
        NUMBER = "number"

    class Status(Enum):
        """
        AutoML 피쳐 상태입니다.

        - CREATED: 생성됨
        - IN_SERVICE: 서비스 중
        - DEPRECATED: 더 이상 지원하지 않음
        """

        CREATED = "created"
        IN_SERVICE = "in_service"
        DEPRECATED = "deprecated"

    def __init__(self, **kwargs):
        """
        AutoML 피쳐 클래스.

        ## Attributes

        - id: (int) 피쳐 ID
        - name: (str) 이름
        - source: (str) 원천 경로
        - type: (`sktmls.ml_features.MLFeature.Type`) 타입
        - status: (`sktmls.ml_features.MLFeature.Status`) 서비스 상태
        - title: (str) 타이틀
        - description: (str) 설명
        - created_at: (datetime.datetime) 생성 시각
        - updated_at: (datetime.datetime) 갱신 시각
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.source = kwargs.get("source")
        self.type = MLFeature.Type(kwargs.get("type"))
        self.type = MLFeature.Status(kwargs.get("status"))
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return f"{self.source}.{self.name}"


class MLFeatureClient(MLSClient):
    def __init__(
        self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, username: str = None, password: str = None
    ):
        """
        AutoML 피쳐 관련 기능을 제공하는 클라이언트 클래스입니다.

        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env
        - $MLS_USERNAME: username
        - $MLS_PASSWORD: password

        ## Returns
        `sktmls.datasets.DatasetClient`

        ## Example

        ```
        client = DatasetClient(env=MLSENV.STG, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_feature(self, name: str, source: str, type: MLFeature.Type, title: str = None, description: str = None):
        """
        새로운 AutoML 피쳐를 생성합니다.

        ## Args

        - name: (str) 이름
        - source: (str) 원천 경로
        - type: (`sktmls.ml_features.MLFeature.Type`) 타입
        - title: (optional) (str) 타이틀
        - description: (optional) (str) 설명

        ## Returns
        `sktmls.ml_features.MLFeature`
        ```
        """
        data = {
            "name": name,
            "source": source,
            "type": type.value,
        }
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        return self._request(method="POST", url="api/v1/ml_features", data=data)
