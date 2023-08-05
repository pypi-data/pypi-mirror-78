CONFIG = {
    "YE": {
        "MLS_API_URL": {
            "dev": "https://ab-internal.dev.sktmls.com",
            "stg": "https://ab-internal.stg.sktmls.com",
            "prd": "https://ab-internal.sktmls.com",
        },
        "HDFS_OPTIONS": "",
    },
    "EDD": {
        "MLS_API_URL": {
            "dev": "https://ab-onprem.dev.sktmls.com",
            "stg": "https://ab-onprem.stg.sktmls.com",
            "prd": "https://ab-onprem.sktmls.com",
        },
        "HDFS_OPTIONS": """-Dfs.s3a.proxy.host=awsproxy.datalake.net \
                 -Dfs.s3a.proxy.port=3128 \
                 -Dfs.s3a.endpoint=s3.ap-northeast-2.amazonaws.com \
                 -Dfs.s3a.security.credential.provider.path=jceks:///user/tairflow/s3_mls.jceks \
                 -Dfs.s3a.fast.upload=true -Dfs.s3a.acl.default=BucketOwnerFullControl""",
    },
    "LOCAL": {
        "MLS_API_URL": {
            "local": "http://ab.local.sktmls.com:8000",
            "dev": "https://ab.dev.sktmls.com",
            "stg": "https://ab.stg.sktmls.com",
            "prd": "https://ab.sktmls.com",
        },
        "HDFS_OPTIONS": "",
    },
}


class Config:
    def __init__(self, runtime_env: str):
        setattr(self, "MLS_RUNTIME_ENV", runtime_env)

        for key, value in CONFIG.get(runtime_env).items():
            setattr(self, key, value)
