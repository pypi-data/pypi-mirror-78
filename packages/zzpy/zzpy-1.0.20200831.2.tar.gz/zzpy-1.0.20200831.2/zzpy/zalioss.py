import re
import oss2

__OSS_URL_KEY = "OSS_URL"


class OssConfig:
    def __init__(self, url):
        result = re.search("^(oss://){0,1}([^/]+)/([^?]+)\?(.*)$", url)
        groups = result.groups()
        endpoint = f"https://{groups[1]}"
        assert endpoint
        bucket = groups[2]
        assert bucket
        param = dict([it.split('=')
                      for it in groups[3].split('&')])
        assert param
        access_key_id = param.get("key")
        assert access_key_id
        access_key_secret = param.get("secret")
        assert access_key_secret

        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.bucket = bucket
        self.endpoint = endpoint


def oss_connect(url=None):
    if not url:
        from .zconfig import get_param
        url = get_param(__OSS_URL_KEY)
    assert url

    return AliOss(url)


class AliOss:
    def __init__(self, url):
        config = OssConfig(url)
        self.config = config
        self.bucket = oss2.Bucket(
            oss2.Auth(config.access_key_id, config.access_key_secret), config.endpoint, config.bucket)
        self.show_progress = False
        self.progress = None

    def url(self, key):
        return f"oss://{self.config.bucket}/{key}"

    def download(self, key, file_path, show_progress=False):
        """下载文件"""
        self.show_progress = show_progress
        if show_progress:
            from .zprogress import pb
            self.progress = pb(total=100, title="下载")
        else:
            self.progress = None
        return self.bucket.get_object_to_file(key, file_path, progress_callback=self.progress_callback)

    def progress_callback(self, done, total):
        if self.show_progress and self.progress:
            self.progress.n=done
            self.progress.refresh()

    def upload(self, key, file_path, infrequent_access_flag=True, show_progress=False):
        """上传文件，infrequent_access_flag低频标识"""
        import oss2
        headers = {
            'x-oss-storage-class': oss2.BUCKET_STORAGE_CLASS_IA} if infrequent_access_flag else None
        self.show_progress = show_progress
        if show_progress:
            from .zprogress import pb
            self.progress = pb(total=100, title="上传")
        else:
            self.progress = None
        return self.bucket.put_object_from_file(key, file_path, progress_callback=self.progress_callback)

    def list(self, prefix):
        next_marker = ""
        while True:
            result = self.bucket.list_objects(
                prefix=prefix, max_keys=1_000, marker=next_marker)
            for it in result.object_list:
                yield it.key
            next_marker = result.next_marker
            if not next_marker:
                break

    def delete(self, prefix):
        for key in self.list():
            self.bucket.delete_object(key=key)

    def exist(self, key):
        """判断文件是否已存在"""
        return self.bucket.object_exists(key)

    def not_exist(self, key):
        """判断文件是否不存在"""
        return not self.exist(key)

    def meta(self, key):
        """获取文件元信息"""
        return self.bucket.get_object_meta(key)
