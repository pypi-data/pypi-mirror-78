CONFIG = {
    "YE": {
        "MLS_AB_API_URL": {
            "dev": "https://ab-internal.dev.sktmls.com",
            "stg": "https://ab-internal.stg.sktmls.com",
            "prd": "https://ab-internal.sktmls.com",
        },
        "MLS_PROFILE_API_URL": {
            "dev": "https://pf-internal.dev.sktmls.com",
            "stg": "https://pf-internal.stg.sktmls.com",
            "prd": "https://pf-internal.sktmls.com",
        },
        "HDFS_OPTIONS": "",
    },
    "EDD": {
        "MLS_AB_API_URL": {
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
    "MMS": {
        "MLS_PROFILE_API_URL": {
            "dev": "http://mls-up-nlb-c1258767e988aad3.elb.ap-northeast-2.amazonaws.com:8080",
            "stg": "http://mls-up-nlb-14dacbe8358f4ba2.elb.ap-northeast-2.amazonaws.com:8080",
            "prd": "http://mls-up-nlb-c0a691baaeae6cdb.elb.ap-northeast-2.amazonaws.com:8080",
        }
    },
    "LOCAL": {
        "MLS_AB_API_URL": {
            "local": "http://ab.local.sktmls.com:8000",
            "dev": "https://ab.dev.sktmls.com",
            "stg": "https://ab.stg.sktmls.com",
            "prd": "https://ab.sktmls.com",
        },
        "MLS_PROFILE_API_URL": {
            "local": "https://pf.dev.sktmls.com",
            "dev": "https://pf.dev.sktmls.com",
            "stg": "https://pf.stg.sktmls.com",
            "prd": "https://pf.sktmls.com",
        },
        "HDFS_OPTIONS": "",
    },
}


class Config:
    def __init__(self, runtime_env: str):
        setattr(self, "MLS_RUNTIME_ENV", runtime_env)

        for key, value in CONFIG.get(runtime_env).items():
            setattr(self, key, value)
