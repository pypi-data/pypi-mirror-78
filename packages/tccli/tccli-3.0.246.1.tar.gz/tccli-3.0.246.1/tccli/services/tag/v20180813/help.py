# -*- coding: utf-8 -*-
DESC = "tag-2018-08-13"
INFO = {
  "DescribeResourceTagsByTagKeys": {
    "params": [
      {
        "name": "ServiceType",
        "desc": "业务类型"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源地域"
      },
      {
        "name": "ResourceIds",
        "desc": "资源唯一标识"
      },
      {
        "name": "TagKeys",
        "desc": "资源标签键"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 400"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      }
    ],
    "desc": "根据标签键获取资源标签"
  },
  "DescribeResourceTagsByResourceIdsSeq": {
    "params": [
      {
        "name": "ServiceType",
        "desc": "业务类型"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀"
      },
      {
        "name": "ResourceIds",
        "desc": "资源唯一标记"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      }
    ],
    "desc": "按顺序查看资源关联的标签"
  },
  "DetachResourcesTag": {
    "params": [
      {
        "name": "ServiceType",
        "desc": "资源所属业务名称"
      },
      {
        "name": "ResourceIds",
        "desc": "资源ID数组，资源个数最多为50"
      },
      {
        "name": "TagKey",
        "desc": "需要解绑的标签键"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域不区分地域的资源不需要传入该字段"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀，cos存储桶不需要传入该字段"
      }
    ],
    "desc": "解绑多个资源关联的某个标签"
  },
  "DescribeTagValues": {
    "params": [
      {
        "name": "TagKeys",
        "desc": "标签键列表"
      },
      {
        "name": "CreateUin",
        "desc": "创建者用户 Uin，不传或为空只将 Uin 作为条件查询"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      }
    ],
    "desc": "用于查询已建立的标签列表中的标签值。"
  },
  "DescribeResourceTagsByResourceIds": {
    "params": [
      {
        "name": "ServiceType",
        "desc": "业务类型"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀"
      },
      {
        "name": "ResourceIds",
        "desc": "资源唯一标记"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      }
    ],
    "desc": "用于查询已有资源标签键值对"
  },
  "DescribeResourceTags": {
    "params": [
      {
        "name": "CreateUin",
        "desc": "创建者uin"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域"
      },
      {
        "name": "ServiceType",
        "desc": "业务类型"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀"
      },
      {
        "name": "ResourceId",
        "desc": "资源唯一标识"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      },
      {
        "name": "CosResourceId",
        "desc": "是否是Cos的资源id"
      }
    ],
    "desc": "查询资源关联标签"
  },
  "AddResourceTag": {
    "params": [
      {
        "name": "TagKey",
        "desc": "标签键"
      },
      {
        "name": "TagValue",
        "desc": "标签值"
      },
      {
        "name": "Resource",
        "desc": "[ 资源六段式描述 ](https://cloud.tencent.com/document/product/598/10606)"
      }
    ],
    "desc": "本接口用于给标签关联资源"
  },
  "UpdateResourceTagValue": {
    "params": [
      {
        "name": "TagKey",
        "desc": "资源关联的标签键"
      },
      {
        "name": "TagValue",
        "desc": "修改后的标签值"
      },
      {
        "name": "Resource",
        "desc": "[ 资源六段式描述 ](https://cloud.tencent.com/document/product/598/10606)"
      }
    ],
    "desc": "本接口用于修改资源已关联的标签值（标签键不变）"
  },
  "DeleteResourceTag": {
    "params": [
      {
        "name": "TagKey",
        "desc": "标签键"
      },
      {
        "name": "Resource",
        "desc": "[ 资源六段式描述 ](https://cloud.tencent.com/document/product/598/10606)"
      }
    ],
    "desc": "本接口用于解除标签和资源的关联关系"
  },
  "DescribeResourcesByTagsUnion": {
    "params": [
      {
        "name": "TagFilters",
        "desc": "标签过滤数组"
      },
      {
        "name": "CreateUin",
        "desc": "创建标签者uin"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀"
      },
      {
        "name": "ResourceId",
        "desc": "资源唯一标记"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域"
      },
      {
        "name": "ServiceType",
        "desc": "业务类型"
      }
    ],
    "desc": "通过标签查询资源列表并集"
  },
  "DescribeTagValuesSeq": {
    "params": [
      {
        "name": "TagKeys",
        "desc": "标签键列表"
      },
      {
        "name": "CreateUin",
        "desc": "创建者用户 Uin，不传或为空只将 Uin 作为条件查询"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      }
    ],
    "desc": "用于查询已建立的标签列表中的标签值。"
  },
  "DescribeTags": {
    "params": [
      {
        "name": "TagKey",
        "desc": "标签键,与标签值同时存在或同时不存在，不存在时表示查询该用户所有标签"
      },
      {
        "name": "TagValue",
        "desc": "标签值,与标签键同时存在或同时不存在，不存在时表示查询该用户所有标签"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      },
      {
        "name": "CreateUin",
        "desc": "创建者用户 Uin，不传或为空只将 Uin 作为条件查询"
      },
      {
        "name": "TagKeys",
        "desc": "标签键数组,与标签值同时存在或同时不存在，不存在时表示查询该用户所有标签,当与TagKey同时传递时只取本值"
      },
      {
        "name": "ShowProject",
        "desc": "是否展现项目标签"
      }
    ],
    "desc": "用于查询已建立的标签列表。\n"
  },
  "DescribeTagsSeq": {
    "params": [
      {
        "name": "TagKey",
        "desc": "标签键,与标签值同时存在或同时不存在，不存在时表示查询该用户所有标签"
      },
      {
        "name": "TagValue",
        "desc": "标签值,与标签键同时存在或同时不存在，不存在时表示查询该用户所有标签"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      },
      {
        "name": "CreateUin",
        "desc": "创建者用户 Uin，不传或为空只将 Uin 作为条件查询"
      },
      {
        "name": "TagKeys",
        "desc": "标签键数组,与标签值同时存在或同时不存在，不存在时表示查询该用户所有标签,当与TagKey同时传递时只取本值"
      },
      {
        "name": "ShowProject",
        "desc": "是否展现项目标签"
      }
    ],
    "desc": "用于查询已建立的标签列表。\n"
  },
  "ModifyResourceTags": {
    "params": [
      {
        "name": "Resource",
        "desc": "[ 资源六段式描述 ](https://cloud.tencent.com/document/product/598/10606)"
      },
      {
        "name": "ReplaceTags",
        "desc": "需要增加或修改的标签集合。如果Resource描述的资源未关联输入的标签键，则增加关联；若已关联，则将该资源关联的键对应的标签值修改为输入值。本接口中ReplaceTags和DeleteTags二者必须存在其一，且二者不能包含相同的标签键"
      },
      {
        "name": "DeleteTags",
        "desc": "需要解关联的标签集合。本接口中ReplaceTags和DeleteTags二者必须存在其一，且二者不能包含相同的标签键"
      }
    ],
    "desc": "本接口用于修改资源关联的所有标签"
  },
  "DescribeResourcesByTags": {
    "params": [
      {
        "name": "TagFilters",
        "desc": "标签过滤数组"
      },
      {
        "name": "CreateUin",
        "desc": "创建标签者uin"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀"
      },
      {
        "name": "ResourceId",
        "desc": "资源唯一标记"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域"
      },
      {
        "name": "ServiceType",
        "desc": "业务类型"
      }
    ],
    "desc": "通过标签查询资源列表"
  },
  "DescribeTagKeys": {
    "params": [
      {
        "name": "CreateUin",
        "desc": "创建者用户 Uin，不传或为空只将 Uin 作为条件查询"
      },
      {
        "name": "Offset",
        "desc": "数据偏移量，默认为 0, 必须为Limit参数的整数倍"
      },
      {
        "name": "Limit",
        "desc": "每页大小，默认为 15"
      },
      {
        "name": "ShowProject",
        "desc": "是否展现项目"
      }
    ],
    "desc": "用于查询已建立的标签列表中的标签键。\n"
  },
  "AttachResourcesTag": {
    "params": [
      {
        "name": "ServiceType",
        "desc": "资源所属业务名称"
      },
      {
        "name": "ResourceIds",
        "desc": "资源ID数组，资源个数最多为50"
      },
      {
        "name": "TagKey",
        "desc": "标签键"
      },
      {
        "name": "TagValue",
        "desc": "标签值"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域，不区分地域的资源不需要传入该字段"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀，cos存储桶不需要传入该字段"
      }
    ],
    "desc": "给多个资源关联某个标签"
  },
  "DeleteTag": {
    "params": [
      {
        "name": "TagKey",
        "desc": "需要删除的标签键"
      },
      {
        "name": "TagValue",
        "desc": "需要删除的标签值"
      }
    ],
    "desc": "本接口用于删除一对标签键和标签值"
  },
  "CreateTag": {
    "params": [
      {
        "name": "TagKey",
        "desc": "标签键"
      },
      {
        "name": "TagValue",
        "desc": "标签值"
      }
    ],
    "desc": "本接口用于创建一对标签键和标签值"
  },
  "ModifyResourcesTagValue": {
    "params": [
      {
        "name": "ServiceType",
        "desc": "资源所属业务名称"
      },
      {
        "name": "ResourceIds",
        "desc": "资源ID数组，资源个数最多为50"
      },
      {
        "name": "TagKey",
        "desc": "标签键"
      },
      {
        "name": "TagValue",
        "desc": "标签值"
      },
      {
        "name": "ResourceRegion",
        "desc": "资源所在地域，不区分地域的资源不需要传入该字段"
      },
      {
        "name": "ResourcePrefix",
        "desc": "资源前缀，cos存储桶不需要传入该字段"
      }
    ],
    "desc": "修改多个资源关联的某个标签键对应的标签值"
  }
}