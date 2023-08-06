# -*- coding: utf-8 -*-
DESC = "cloudaudit-2019-03-19"
INFO = {
  "StartLogging": {
    "params": [
      {
        "name": "AuditName",
        "desc": "跟踪集名称"
      }
    ],
    "desc": "开启跟踪集"
  },
  "GetAttributeKey": {
    "params": [
      {
        "name": "WebsiteType",
        "desc": "网站类型，取值范围是zh和en。如果不传值默认zh"
      }
    ],
    "desc": "查询AttributeKey的有效取值范围"
  },
  "ListCmqEnableRegion": {
    "params": [
      {
        "name": "WebsiteType",
        "desc": "站点类型。zh表示中国区，en表示国际区。默认中国区。"
      }
    ],
    "desc": "查询云审计支持的cmq的可用区"
  },
  "DeleteAudit": {
    "params": [
      {
        "name": "AuditName",
        "desc": "跟踪集名称"
      }
    ],
    "desc": "删除跟踪集"
  },
  "StopLogging": {
    "params": [
      {
        "name": "AuditName",
        "desc": "跟踪集名称"
      }
    ],
    "desc": "关闭跟踪集"
  },
  "InquireAuditCredit": {
    "params": [],
    "desc": "查询用户可创建跟踪集的数量"
  },
  "UpdateAudit": {
    "params": [
      {
        "name": "AuditName",
        "desc": "跟踪集名称"
      },
      {
        "name": "CmqQueueName",
        "desc": "队列名称。队列名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。如果IsEnableCmqNotify值是1的话，此值属于必填字段。如果不是新创建的队列，云审计不会去校验该队列是否真的存在，请谨慎填写，避免日志通知不成功，导致您的数据丢失。"
      },
      {
        "name": "CmqRegion",
        "desc": "队列所在的地域。可以通过ListCmqEnableRegion获取支持的cmq地域。如果IsEnableCmqNotify值是1的话，此值属于必填字段。"
      },
      {
        "name": "CosBucketName",
        "desc": "cos的存储桶名称。仅支持小写英文字母和数字即[a-z，0-9]、中划线“-”及其组合。用户自定义的字符串支持1 - 40个字符。存储桶命名不能以“-”开头或结尾。如果不是新创建的存储桶，云审计不会去校验该存储桶是否真的存在，请谨慎填写，避免日志投递不成功，导致您的数据丢失。"
      },
      {
        "name": "CosRegion",
        "desc": "cos地域。目前支持的地域可以使用ListCosEnableRegion来获取。"
      },
      {
        "name": "IsCreateNewBucket",
        "desc": "是否创建新的cos存储桶。1：是，0：否。"
      },
      {
        "name": "IsCreateNewQueue",
        "desc": "是否创建新的队列。1：是，0：否。如果IsEnableCmqNotify值是1的话，此值属于必填字段。"
      },
      {
        "name": "IsEnableCmqNotify",
        "desc": "是否开启cmq消息通知。1：是，0：否。目前仅支持cmq的队列服务。如果开启cmq消息通知服务，云审计会将您的日志内容实时投递到您指定地域的指定队列中。"
      },
      {
        "name": "IsEnableKmsEncry",
        "desc": "是否开启kms加密。1：是，0：否。如果开启KMS加密，数据在投递到cos时，会将数据加密。"
      },
      {
        "name": "KeyId",
        "desc": "CMK的全局唯一标识符，如果不是新创建的kms，该值是必填值。可以通过ListKeyAliasByRegion来获取。云审计不会校验KeyId的合法性，请您谨慎填写，避免给您的数据造成损失。"
      },
      {
        "name": "KmsRegion",
        "desc": "kms地域。目前支持的地域可以使用ListKmsEnableRegion来获取。必须要和cos的地域保持一致。"
      },
      {
        "name": "LogFilePrefix",
        "desc": "日志文件前缀。3-40个字符，只能包含 ASCII 编码字母 a-z，A-Z，数字 0-9。"
      },
      {
        "name": "ReadWriteAttribute",
        "desc": "管理事件的读写属性。1：只读，2：只写，3：全部。"
      }
    ],
    "desc": "参数要求：\n1、如果IsCreateNewBucket的值存在的话，cosRegion和cosBucketName都是必填参数。\n2、如果IsEnableCmqNotify的值是1的话，IsCreateNewQueue、CmqRegion和CmqQueueName都是必填参数。\n3、如果IsEnableCmqNotify的值是0的话，IsCreateNewQueue、CmqRegion和CmqQueueName都不能传。\n4、如果IsEnableKmsEncry的值是1的话，KmsRegion和KeyId属于必填项"
  },
  "DescribeAudit": {
    "params": [
      {
        "name": "AuditName",
        "desc": "跟踪集名称"
      }
    ],
    "desc": "查询跟踪集详情"
  },
  "CreateAudit": {
    "params": [
      {
        "name": "AuditName",
        "desc": "跟踪集名称。3-128字符，只能包含 ASCII 编码字母 a-z，A-Z，数字 0-9，下划线 _。"
      },
      {
        "name": "CosBucketName",
        "desc": "cos的存储桶名称。仅支持小写英文字母和数字即[a-z，0-9]、中划线“-”及其组合。用户自定义的字符串支持1 - 40个字符。存储桶命名不能以“-”开头或结尾。如果不是新创建的存储桶，云审计不会去校验该存储桶是否真的存在，请谨慎填写，避免日志投递不成功，导致您的数据丢失。"
      },
      {
        "name": "CosRegion",
        "desc": "cos地域。目前支持的地域可以使用ListCosEnableRegion来获取。"
      },
      {
        "name": "IsCreateNewBucket",
        "desc": "是否创建新的cos存储桶。1：是，0：否。"
      },
      {
        "name": "IsEnableCmqNotify",
        "desc": "是否开启cmq消息通知。1：是，0：否。目前仅支持cmq的队列服务。如果开启cmq消息通知服务，云审计会将您的日志内容实时投递到您指定地域的指定队列中。"
      },
      {
        "name": "ReadWriteAttribute",
        "desc": "管理事件的读写属性。1：只读，2：只写，3：全部。"
      },
      {
        "name": "CmqQueueName",
        "desc": "队列名称。队列名称是一个不超过64个字符的字符串，必须以字母为首字符，剩余部分可以包含字母、数字和横划线(-)。如果IsEnableCmqNotify值是1的话，此值属于必填字段。如果不是新创建的队列，云审计不会去校验该队列是否真的存在，请谨慎填写，避免日志通知不成功，导致您的数据丢失。"
      },
      {
        "name": "CmqRegion",
        "desc": "队列所在的地域。可以通过ListCmqEnableRegion获取支持的cmq地域。如果IsEnableCmqNotify值是1的话，此值属于必填字段。"
      },
      {
        "name": "IsCreateNewQueue",
        "desc": "是否创建新的队列。1：是，0：否。如果IsEnableCmqNotify值是1的话，此值属于必填字段。"
      },
      {
        "name": "IsEnableKmsEncry",
        "desc": "是否开启kms加密。1：是，0：否。如果开启KMS加密，数据在投递到cos时，会将数据加密。"
      },
      {
        "name": "KeyId",
        "desc": "CMK的全局唯一标识符，如果不是新创建的kms，该值是必填值。可以通过ListKeyAliasByRegion来获取。云审计不会校验KeyId的合法性，请您谨慎填写，避免给您的数据造成损失。"
      },
      {
        "name": "KmsRegion",
        "desc": "kms地域。目前支持的地域可以使用ListKmsEnableRegion来获取。必须要和cos的地域保持一致。"
      },
      {
        "name": "LogFilePrefix",
        "desc": "日志文件前缀。3-40个字符，只能包含 ASCII 编码字母 a-z，A-Z，数字 0-9。可以不填，默认以账号ID作为日志前缀。"
      }
    ],
    "desc": "参数要求：\n1、如果IsCreateNewBucket的值存在的话，cosRegion和cosBucketName都是必填参数。\n2、如果IsEnableCmqNotify的值是1的话，IsCreateNewQueue、CmqRegion和CmqQueueName都是必填参数。\n3、如果IsEnableCmqNotify的值是0的话，IsCreateNewQueue、CmqRegion和CmqQueueName都不能传。\n4、如果IsEnableKmsEncry的值是1的话，KmsRegion和KeyId属于必填项"
  },
  "ListCosEnableRegion": {
    "params": [
      {
        "name": "WebsiteType",
        "desc": "站点类型。zh表示中国区，en表示国际区。默认中国区。"
      }
    ],
    "desc": "查询云审计支持的cos可用区"
  },
  "LookUpEvents": {
    "params": [
      {
        "name": "EndTime",
        "desc": "结束时间"
      },
      {
        "name": "StartTime",
        "desc": "开始时间"
      },
      {
        "name": "LookupAttributes",
        "desc": "检索条件"
      },
      {
        "name": "MaxResults",
        "desc": "返回日志的最大条数"
      },
      {
        "name": "Mode",
        "desc": "云审计模式，有效值：standard | quick，其中standard是标准模式，quick是极速模式。默认为标准模式"
      },
      {
        "name": "NextToken",
        "desc": "查看更多日志的凭证"
      }
    ],
    "desc": "用于对操作日志进行检索，便于用户进行查询相关的操作信息。"
  },
  "ListAudits": {
    "params": [],
    "desc": "查询跟踪集概要"
  }
}