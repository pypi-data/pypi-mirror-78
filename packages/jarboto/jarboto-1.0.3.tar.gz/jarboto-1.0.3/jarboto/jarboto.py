import os
import sys
import io
import boto3


class ConfigError(Exception):
    """ Configuration exception """
    pass


class S3Error(Exception):
    """ Captures boto3 exceptions """
    pass


class S3:
    """ Class to wrap S3 operations conditional to environment config """

    def __init__(self, bucket=None, prefix=None):
        '''
        Constructor

        Args:
            bucket: optionally override bucket specified in environment
            prefix: optionally override prefix specified in environment
                    (optional in environmnet as well, defaults to 'output/')

        Notes:
            Throws ConfigError if environment not configured, use that
            as a conditional way to use an alternate method to fetch objects
        '''
        accesskey = os.environ.get('JARVICE_S3_ACCESSKEY', None)
        secretkey = os.environ.get('JARVICE_S3_SECRETKEY', None)
        bucket = bucket if bucket else os.environ.get('JARVICE_S3_BUCKET',
                                                      None)
        prefix = prefix if prefix else os.environ.get('JARVICE_S3_PREFIX',
                                                      'output/')

        # accesskey, secretkey, and bucket are mandatory
        if accesskey and secretkey and bucket:
            self.s3 = boto3.resource('s3', aws_access_key_id=accesskey,
                                     aws_secret_access_key=secretkey,
                                     region_name=os.environ.get(
                                         'JARVICE_S3_REGION', None),
                                     endpoint_url=os.environ.get(
                                         'JARVICE_S3_ENDPOINTURL', None))
            self.bucket = self.s3.Bucket(bucket)
            self.bucketname = bucket
            self.prefix = prefix
        else:
            raise ConfigError('S3 access not configured in environment')

    def getf(self, name, f):
        '''
        GET object contents to a file or stream

        Args:
            name:   object name (minus prefix)
            f:      file or stream (must be writeable)
        '''
        try:
            self.bucket.download_fileobj((self.prefix + name).lower(), f)
        except Exception as e:
            raise S3Error(e)

    def get(self, name):
        '''
        GET object contents as a buffer

        Args:
            name:   object name (minus prefix)

        Returns:
            buffer with object contents if successful
        '''
        f = io.BytesIO()
        self.getf(name, f)
        f.seek(0)
        return f.read()

    def putf(self, name, f):
        '''
        PUT a file or stream as an object

        Args:
            name:   object name (minus prefix)
            f:      file or stream (must be readable)
        '''
        try:
            self.bucket.upload_fileobj(f, (self.prefix + name).lower())
        except Exception as e:
            raise
            raise S3Error(e)

    def put(self, name, buf):
        '''
        PUT object contents as a buffer

        Args:
            name:   object name (minus prefix)
            buf:    buffer with contents
        '''
        f = io.BytesIO(buf)
        self.putf(name, f)


# unit test (specify get/put as argv[1], object name as argv[2])
if __name__ == '__main__':
    try:
        op = sys.argv[1]
        name = sys.argv[2]
        assert(op == 'get' or op == 'put')
    except Exception:
        sys.stderr.write(
            'usage: python[3] ./jarboto <get|put> <object-name>\n')
        sys.exit(1)

    try:
        if op == 'get':
            S3().getf(name, sys.stdout.buffer if sys.version_info >= (3, 0)
                      else sys.stdout)
        else:
            S3().putf(name, sys.stdin.buffer if sys.version_info >= (3, 0)
                      else sys.stdin)
    except S3Error as e:
        sys.stderr.write(op + ': ' + str(e) + '\n')
        sys.exit(1)
    except ConfigError as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(1)

    sys.exit(0)
