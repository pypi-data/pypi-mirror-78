

{
    'Findings': [
        {
            'SchemaVersion': 'string',
            'Id': 'string',
            'ProductArn': 'string',
            'GeneratorId': 'string',
            'AwsAccountId': 'string',
            'Types': [
                'string',
            ],
            'FirstObservedAt': 'string',
            'LastObservedAt': 'string',
            'CreatedAt': 'string',
            'UpdatedAt': 'string',
            'Severity': {
                'Product': 123.0,
                'Label': 'INFORMATIONAL'|'LOW'|'MEDIUM'|'HIGH'|'CRITICAL',
                'Normalized': 123,
                'Original': 'string'
            },
            'Confidence': 123,
            'Criticality': 123,
            'Title': 'string',
            'Description': 'string',
            'Remediation': {
                'Recommendation': {
                    'Text': 'string',
                    'Url': 'string'
                }
            },
            'SourceUrl': 'string',
            'ProductFields': {
                'string': 'string'
            },
            'UserDefinedFields': {
                'string': 'string'
            },
            'Malware': [
                {
                    'Name': 'string',
                    'Type': 'ADWARE'|'BLENDED_THREAT'|'BOTNET_AGENT'|'COIN_MINER'|'EXPLOIT_KIT'|'KEYLOGGER'|'MACRO'|'POTENTIALLY_UNWANTED'|'SPYWARE'|'RANSOMWARE'|'REMOTE_ACCESS'|'ROOTKIT'|'TROJAN'|'VIRUS'|'WORM',
                    'Path': 'string',
                    'State': 'OBSERVED'|'REMOVAL_FAILED'|'REMOVED'
                },
            ],
            'Network': {
                'Direction': 'IN'|'OUT',
                'Protocol': 'string',
                'OpenPortRange': {
                    'Begin': 123,
                    'End': 123
                },
                'SourceIpV4': 'string',
                'SourceIpV6': 'string',
                'SourcePort': 123,
                'SourceDomain': 'string',
                'SourceMac': 'string',
                'DestinationIpV4': 'string',
                'DestinationIpV6': 'string',
                'DestinationPort': 123,
                'DestinationDomain': 'string'
            },
            'NetworkPath': [
                {
                    'ComponentId': 'string',
                    'ComponentType': 'string',
                    'Egress': {
                        'Protocol': 'string',
                        'Destination': {
                            'Address': [
                                'string',
                            ],
                            'PortRanges': [
                                {
                                    'Begin': 123,
                                    'End': 123
                                },
                            ]
                        },
                        'Source': {
                            'Address': [
                                'string',
                            ],
                            'PortRanges': [
                                {
                                    'Begin': 123,
                                    'End': 123
                                },
                            ]
                        }
                    },
                    'Ingress': {
                        'Protocol': 'string',
                        'Destination': {
                            'Address': [
                                'string',
                            ],
                            'PortRanges': [
                                {
                                    'Begin': 123,
                                    'End': 123
                                },
                            ]
                        },
                        'Source': {
                            'Address': [
                                'string',
                            ],
                            'PortRanges': [
                                {
                                    'Begin': 123,
                                    'End': 123
                                },
                            ]
                        }
                    }
                },
            ],
            'Process': {
                'Name': 'string',
                'Path': 'string',
                'Pid': 123,
                'ParentPid': 123,
                'LaunchedAt': 'string',
                'TerminatedAt': 'string'
            },
            'ThreatIntelIndicators': [
                {
                    'Type': 'DOMAIN'|'EMAIL_ADDRESS'|'HASH_MD5'|'HASH_SHA1'|'HASH_SHA256'|'HASH_SHA512'|'IPV4_ADDRESS'|'IPV6_ADDRESS'|'MUTEX'|'PROCESS'|'URL',
                    'Value': 'string',
                    'Category': 'BACKDOOR'|'CARD_STEALER'|'COMMAND_AND_CONTROL'|'DROP_SITE'|'EXPLOIT_SITE'|'KEYLOGGER',
                    'LastObservedAt': 'string',
                    'Source': 'string',
                    'SourceUrl': 'string'
                },
            ],
            'Resources': [
                {
                    'Type': 'string',
                    'Id': 'string',
                    'Partition': 'aws'|'aws-cn'|'aws-us-gov',
                    'Region': 'string',
                    'Tags': {
                        'string': 'string'
                    },
                    'Details': {
                        'AwsAutoScalingAutoScalingGroup': {
                            'LaunchConfigurationName': 'string',
                            'LoadBalancerNames': [
                                'string',
                            ],
                            'HealthCheckType': 'string',
                            'HealthCheckGracePeriod': 123,
                            'CreatedTime': 'string'
                        },
                        'AwsCodeBuildProject': {
                            'EncryptionKey': 'string',
                            'Environment': {
                                'Certificate': 'string',
                                'ImagePullCredentialsType': 'string',
                                'RegistryCredential': {
                                    'Credential': 'string',
                                    'CredentialProvider': 'string'
                                },
                                'Type': 'string'
                            },
                            'Name': 'string',
                            'Source': {
                                'Type': 'string',
                                'Location': 'string',
                                'GitCloneDepth': 123,
                                'InsecureSsl': True|False
                            },
                            'ServiceRole': 'string',
                            'VpcConfig': {
                                'VpcId': 'string',
                                'Subnets': [
                                    'string',
                                ],
                                'SecurityGroupIds': [
                                    'string',
                                ]
                            }
                        },
                        'AwsCloudFrontDistribution': {
                            'DomainName': 'string',
                            'ETag': 'string',
                            'LastModifiedTime': 'string',
                            'Logging': {
                                'Bucket': 'string',
                                'Enabled': True|False,
                                'IncludeCookies': True|False,
                                'Prefix': 'string'
                            },
                            'Origins': {
                                'Items': [
                                    {
                                        'DomainName': 'string',
                                        'Id': 'string',
                                        'OriginPath': 'string'
                                    },
                                ]
                            },
                            'Status': 'string',
                            'WebAclId': 'string'
                        },
                        'AwsEc2Instance': {
                            'Type': 'string',
                            'ImageId': 'string',
                            'IpV4Addresses': [
                                'string',
                            ],
                            'IpV6Addresses': [
                                'string',
                            ],
                            'KeyName': 'string',
                            'IamInstanceProfileArn': 'string',
                            'VpcId': 'string',
                            'SubnetId': 'string',
                            'LaunchedAt': 'string'
                        },
                        'AwsEc2NetworkInterface': {
                            'Attachment': {
                                'AttachTime': 'string',
                                'AttachmentId': 'string',
                                'DeleteOnTermination': True|False,
                                'DeviceIndex': 123,
                                'InstanceId': 'string',
                                'InstanceOwnerId': 'string',
                                'Status': 'string'
                            },
                            'NetworkInterfaceId': 'string',
                            'SecurityGroups': [
                                {
                                    'GroupName': 'string',
                                    'GroupId': 'string'
                                },
                            ],
                            'SourceDestCheck': True|False
                        },
                        'AwsEc2SecurityGroup': {
                            'GroupName': 'string',
                            'GroupId': 'string',
                            'OwnerId': 'string',
                            'VpcId': 'string',
                            'IpPermissions': [
                                {
                                    'IpProtocol': 'string',
                                    'FromPort': 123,
                                    'ToPort': 123,
                                    'UserIdGroupPairs': [
                                        {
                                            'GroupId': 'string',
                                            'GroupName': 'string',
                                            'PeeringStatus': 'string',
                                            'UserId': 'string',
                                            'VpcId': 'string',
                                            'VpcPeeringConnectionId': 'string'
                                        },
                                    ],
                                    'IpRanges': [
                                        {
                                            'CidrIp': 'string'
                                        },
                                    ],
                                    'Ipv6Ranges': [
                                        {
                                            'CidrIpv6': 'string'
                                        },
                                    ],
                                    'PrefixListIds': [
                                        {
                                            'PrefixListId': 'string'
                                        },
                                    ]
                                },
                            ],
                            'IpPermissionsEgress': [
                                {
                                    'IpProtocol': 'string',
                                    'FromPort': 123,
                                    'ToPort': 123,
                                    'UserIdGroupPairs': [
                                        {
                                            'GroupId': 'string',
                                            'GroupName': 'string',
                                            'PeeringStatus': 'string',
                                            'UserId': 'string',
                                            'VpcId': 'string',
                                            'VpcPeeringConnectionId': 'string'
                                        },
                                    ],
                                    'IpRanges': [
                                        {
                                            'CidrIp': 'string'
                                        },
                                    ],
                                    'Ipv6Ranges': [
                                        {
                                            'CidrIpv6': 'string'
                                        },
                                    ],
                                    'PrefixListIds': [
                                        {
                                            'PrefixListId': 'string'
                                        },
                                    ]
                                },
                            ]
                        },
                        'AwsEc2Volume': {
                            'CreateTime': 'string',
                            'Encrypted': True|False,
                            'Size': 123,
                            'SnapshotId': 'string',
                            'Status': 'string',
                            'KmsKeyId': 'string',
                            'Attachments': [
                                {
                                    'AttachTime': 'string',
                                    'DeleteOnTermination': True|False,
                                    'InstanceId': 'string',
                                    'Status': 'string'
                                },
                            ]
                        },
                        'AwsEc2Vpc': {
                            'CidrBlockAssociationSet': [
                                {
                                    'AssociationId': 'string',
                                    'CidrBlock': 'string',
                                    'CidrBlockState': 'string'
                                },
                            ],
                            'Ipv6CidrBlockAssociationSet': [
                                {
                                    'AssociationId': 'string',
                                    'Ipv6CidrBlock': 'string',
                                    'CidrBlockState': 'string'
                                },
                            ],
                            'DhcpOptionsId': 'string',
                            'State': 'string'
                        },
                        'AwsEc2Eip': {
                            'InstanceId': 'string',
                            'PublicIp': 'string',
                            'AllocationId': 'string',
                            'AssociationId': 'string',
                            'Domain': 'string',
                            'PublicIpv4Pool': 'string',
                            'NetworkBorderGroup': 'string',
                            'NetworkInterfaceId': 'string',
                            'NetworkInterfaceOwnerId': 'string',
                            'PrivateIpAddress': 'string'
                        },
                        'AwsElbv2LoadBalancer': {
                            'AvailabilityZones': [
                                {
                                    'ZoneName': 'string',
                                    'SubnetId': 'string'
                                },
                            ],
                            'CanonicalHostedZoneId': 'string',
                            'CreatedTime': 'string',
                            'DNSName': 'string',
                            'IpAddressType': 'string',
                            'Scheme': 'string',
                            'SecurityGroups': [
                                'string',
                            ],
                            'State': {
                                'Code': 'string',
                                'Reason': 'string'
                            },
                            'Type': 'string',
                            'VpcId': 'string'
                        },
                        'AwsElasticsearchDomain': {
                            'AccessPolicies': 'string',
                            'DomainEndpointOptions': {
                                'EnforceHTTPS': True|False,
                                'TLSSecurityPolicy': 'string'
                            },
                            'DomainId': 'string',
                            'DomainName': 'string',
                            'Endpoint': 'string',
                            'Endpoints': {
                                'string': 'string'
                            },
                            'ElasticsearchVersion': 'string',
                            'EncryptionAtRestOptions': {
                                'Enabled': True|False,
                                'KmsKeyId': 'string'
                            },
                            'NodeToNodeEncryptionOptions': {
                                'Enabled': True|False
                            },
                            'VPCOptions': {
                                'AvailabilityZones': [
                                    'string',
                                ],
                                'SecurityGroupIds': [
                                    'string',
                                ],
                                'SubnetIds': [
                                    'string',
                                ],
                                'VPCId': 'string'
                            }
                        },
                        'AwsS3Bucket': {
                            'OwnerId': 'string',
                            'OwnerName': 'string',
                            'CreatedAt': 'string',
                            'ServerSideEncryptionConfiguration': {
                                'Rules': [
                                    {
                                        'ApplyServerSideEncryptionByDefault': {
                                            'SSEAlgorithm': 'string',
                                            'KMSMasterKeyID': 'string'
                                        }
                                    },
                                ]
                            }
                        },
                        'AwsS3Object': {
                            'LastModified': 'string',
                            'ETag': 'string',
                            'VersionId': 'string',
                            'ContentType': 'string',
                            'ServerSideEncryption': 'string',
                            'SSEKMSKeyId': 'string'
                        },
                        'AwsSecretsManagerSecret': {
                            'RotationRules': {
                                'AutomaticallyAfterDays': 123
                            },
                            'RotationOccurredWithinFrequency': True|False,
                            'KmsKeyId': 'string',
                            'RotationEnabled': True|False,
                            'RotationLambdaArn': 'string',
                            'Deleted': True|False,
                            'Name': 'string',
                            'Description': 'string'
                        },
                        'AwsIamAccessKey': {
                            'UserName': 'string',
                            'Status': 'Active'|'Inactive',
                            'CreatedAt': 'string',
                            'PrincipalId': 'string',
                            'PrincipalType': 'string',
                            'PrincipalName': 'string'
                        },
                        'AwsIamUser': {
                            'AttachedManagedPolicies': [
                                {
                                    'PolicyName': 'string',
                                    'PolicyArn': 'string'
                                },
                            ],
                            'CreateDate': 'string',
                            'GroupList': [
                                'string',
                            ],
                            'Path': 'string',
                            'PermissionsBoundary': {
                                'PermissionsBoundaryArn': 'string',
                                'PermissionsBoundaryType': 'string'
                            },
                            'UserId': 'string',
                            'UserName': 'string',
                            'UserPolicyList': [
                                {
                                    'PolicyName': 'string'
                                },
                            ]
                        },
                        'AwsIamPolicy': {
                            'AttachmentCount': 123,
                            'CreateDate': 'string',
                            'DefaultVersionId': 'string',
                            'Description': 'string',
                            'IsAttachable': True|False,
                            'Path': 'string',
                            'PermissionsBoundaryUsageCount': 123,
                            'PolicyId': 'string',
                            'PolicyName': 'string',
                            'PolicyVersionList': [
                                {
                                    'VersionId': 'string',
                                    'IsDefaultVersion': True|False,
                                    'CreateDate': 'string'
                                },
                            ],
                            'UpdateDate': 'string'
                        },
                        'AwsDynamoDbTable': {
                            'AttributeDefinitions': [
                                {
                                    'AttributeName': 'string',
                                    'AttributeType': 'string'
                                },
                            ],
                            'BillingModeSummary': {
                                'BillingMode': 'string',
                                'LastUpdateToPayPerRequestDateTime': 'string'
                            },
                            'CreationDateTime': 'string',
                            'GlobalSecondaryIndexes': [
                                {
                                    'Backfilling': True|False,
                                    'IndexArn': 'string',
                                    'IndexName': 'string',
                                    'IndexSizeBytes': 123,
                                    'IndexStatus': 'string',
                                    'ItemCount': 123,
                                    'KeySchema': [
                                        {
                                            'AttributeName': 'string',
                                            'KeyType': 'string'
                                        },
                                    ],
                                    'Projection': {
                                        'NonKeyAttributes': [
                                            'string',
                                        ],
                                        'ProjectionType': 'string'
                                    },
                                    'ProvisionedThroughput': {
                                        'LastDecreaseDateTime': 'string',
                                        'LastIncreaseDateTime': 'string',
                                        'NumberOfDecreasesToday': 123,
                                        'ReadCapacityUnits': 123,
                                        'WriteCapacityUnits': 123
                                    }
                                },
                            ],
                            'GlobalTableVersion': 'string',
                            'ItemCount': 123,
                            'KeySchema': [
                                {
                                    'AttributeName': 'string',
                                    'KeyType': 'string'
                                },
                            ],
                            'LatestStreamArn': 'string',
                            'LatestStreamLabel': 'string',
                            'LocalSecondaryIndexes': [
                                {
                                    'IndexArn': 'string',
                                    'IndexName': 'string',
                                    'KeySchema': [
                                        {
                                            'AttributeName': 'string',
                                            'KeyType': 'string'
                                        },
                                    ],
                                    'Projection': {
                                        'NonKeyAttributes': [
                                            'string',
                                        ],
                                        'ProjectionType': 'string'
                                    }
                                },
                            ],
                            'ProvisionedThroughput': {
                                'LastDecreaseDateTime': 'string',
                                'LastIncreaseDateTime': 'string',
                                'NumberOfDecreasesToday': 123,
                                'ReadCapacityUnits': 123,
                                'WriteCapacityUnits': 123
                            },
                            'Replicas': [
                                {
                                    'GlobalSecondaryIndexes': [
                                        {
                                            'IndexName': 'string',
                                            'ProvisionedThroughputOverride': {
                                                'ReadCapacityUnits': 123
                                            }
                                        },
                                    ],
                                    'KmsMasterKeyId': 'string',
                                    'ProvisionedThroughputOverride': {
                                        'ReadCapacityUnits': 123
                                    },
                                    'RegionName': 'string',
                                    'ReplicaStatus': 'string',
                                    'ReplicaStatusDescription': 'string'
                                },
                            ],
                            'RestoreSummary': {
                                'SourceBackupArn': 'string',
                                'SourceTableArn': 'string',
                                'RestoreDateTime': 'string',
                                'RestoreInProgress': True|False
                            },
                            'SseDescription': {
                                'InaccessibleEncryptionDateTime': 'string',
                                'Status': 'string',
                                'SseType': 'string',
                                'KmsMasterKeyArn': 'string'
                            },
                            'StreamSpecification': {
                                'StreamEnabled': True|False,
                                'StreamViewType': 'string'
                            },
                            'TableId': 'string',
                            'TableName': 'string',
                            'TableSizeBytes': 123,
                            'TableStatus': 'string'
                        },
                        'AwsIamRole': {
                            'AssumeRolePolicyDocument': 'string',
                            'CreateDate': 'string',
                            'RoleId': 'string',
                            'RoleName': 'string',
                            'MaxSessionDuration': 123,
                            'Path': 'string'
                        },
                        'AwsKmsKey': {
                            'AWSAccountId': 'string',
                            'CreationDate': 123.0,
                            'KeyId': 'string',
                            'KeyManager': 'string',
                            'KeyState': 'string',
                            'Origin': 'string',
                            'Description': 'string'
                        },
                        'AwsLambdaFunction': {
                            'Code': {
                                'S3Bucket': 'string',
                                'S3Key': 'string',
                                'S3ObjectVersion': 'string',
                                'ZipFile': 'string'
                            },
                            'CodeSha256': 'string',
                            'DeadLetterConfig': {
                                'TargetArn': 'string'
                            },
                            'Environment': {
                                'Variables': {
                                    'string': 'string'
                                },
                                'Error': {
                                    'ErrorCode': 'string',
                                    'Message': 'string'
                                }
                            },
                            'FunctionName': 'string',
                            'Handler': 'string',
                            'KmsKeyArn': 'string',
                            'LastModified': 'string',
                            'Layers': [
                                {
                                    'Arn': 'string',
                                    'CodeSize': 123
                                },
                            ],
                            'MasterArn': 'string',
                            'MemorySize': 123,
                            'RevisionId': 'string',
                            'Role': 'string',
                            'Runtime': 'string',
                            'Timeout': 123,
                            'TracingConfig': {
                                'Mode': 'string'
                            },
                            'VpcConfig': {
                                'SecurityGroupIds': [
                                    'string',
                                ],
                                'SubnetIds': [
                                    'string',
                                ],
                                'VpcId': 'string'
                            },
                            'Version': 'string'
                        },
                        'AwsLambdaLayerVersion': {
                            'Version': 123,
                            'CompatibleRuntimes': [
                                'string',
                            ],
                            'CreatedDate': 'string'
                        },
                        'AwsRdsDbInstance': {
                            'AssociatedRoles': [
                                {
                                    'RoleArn': 'string',
                                    'FeatureName': 'string',
                                    'Status': 'string'
                                },
                            ],
                            'CACertificateIdentifier': 'string',
                            'DBClusterIdentifier': 'string',
                            'DBInstanceIdentifier': 'string',
                            'DBInstanceClass': 'string',
                            'DbInstancePort': 123,
                            'DbiResourceId': 'string',
                            'DBName': 'string',
                            'DeletionProtection': True|False,
                            'Endpoint': {
                                'Address': 'string',
                                'Port': 123,
                                'HostedZoneId': 'string'
                            },
                            'Engine': 'string',
                            'EngineVersion': 'string',
                            'IAMDatabaseAuthenticationEnabled': True|False,
                            'InstanceCreateTime': 'string',
                            'KmsKeyId': 'string',
                            'PubliclyAccessible': True|False,
                            'StorageEncrypted': True|False,
                            'TdeCredentialArn': 'string',
                            'VpcSecurityGroups': [
                                {
                                    'VpcSecurityGroupId': 'string',
                                    'Status': 'string'
                                },
                            ],
                            'MultiAz': True|False,
                            'EnhancedMonitoringResourceArn': 'string',
                            'DbInstanceStatus': 'string',
                            'MasterUsername': 'string',
                            'AllocatedStorage': 123,
                            'PreferredBackupWindow': 'string',
                            'BackupRetentionPeriod': 123,
                            'DbSecurityGroups': [
                                'string',
                            ],
                            'DbParameterGroups': [
                                {
                                    'DbParameterGroupName': 'string',
                                    'ParameterApplyStatus': 'string'
                                },
                            ],
                            'AvailabilityZone': 'string',
                            'DbSubnetGroup': {
                                'DbSubnetGroupName': 'string',
                                'DbSubnetGroupDescription': 'string',
                                'VpcId': 'string',
                                'SubnetGroupStatus': 'string',
                                'Subnets': [
                                    {
                                        'SubnetIdentifier': 'string',
                                        'SubnetAvailabilityZone': {
                                            'Name': 'string'
                                        },
                                        'SubnetStatus': 'string'
                                    },
                                ],
                                'DbSubnetGroupArn': 'string'
                            },
                            'PreferredMaintenanceWindow': 'string',
                            'PendingModifiedValues': {
                                'DbInstanceClass': 'string',
                                'AllocatedStorage': 123,
                                'MasterUserPassword': 'string',
                                'Port': 123,
                                'BackupRetentionPeriod': 123,
                                'MultiAZ': True|False,
                                'EngineVersion': 'string',
                                'LicenseModel': 'string',
                                'Iops': 123,
                                'DbInstanceIdentifier': 'string',
                                'StorageType': 'string',
                                'CaCertificateIdentifier': 'string',
                                'DbSubnetGroupName': 'string',
                                'PendingCloudWatchLogsExports': {
                                    'LogTypesToEnable': [
                                        'string',
                                    ],
                                    'LogTypesToDisable': [
                                        'string',
                                    ]
                                },
                                'ProcessorFeatures': [
                                    {
                                        'Name': 'string',
                                        'Value': 'string'
                                    },
                                ]
                            },
                            'LatestRestorableTime': 'string',
                            'AutoMinorVersionUpgrade': True|False,
                            'ReadReplicaSourceDBInstanceIdentifier': 'string',
                            'ReadReplicaDBInstanceIdentifiers': [
                                'string',
                            ],
                            'ReadReplicaDBClusterIdentifiers': [
                                'string',
                            ],
                            'LicenseModel': 'string',
                            'Iops': 123,
                            'OptionGroupMemberships': [
                                {
                                    'OptionGroupName': 'string',
                                    'Status': 'string'
                                },
                            ],
                            'CharacterSetName': 'string',
                            'SecondaryAvailabilityZone': 'string',
                            'StatusInfos': [
                                {
                                    'StatusType': 'string',
                                    'Normal': True|False,
                                    'Status': 'string',
                                    'Message': 'string'
                                },
                            ],
                            'StorageType': 'string',
                            'DomainMemberships': [
                                {
                                    'Domain': 'string',
                                    'Status': 'string',
                                    'Fqdn': 'string',
                                    'IamRoleName': 'string'
                                },
                            ],
                            'CopyTagsToSnapshot': True|False,
                            'MonitoringInterval': 123,
                            'MonitoringRoleArn': 'string',
                            'PromotionTier': 123,
                            'Timezone': 'string',
                            'PerformanceInsightsEnabled': True|False,
                            'PerformanceInsightsKmsKeyId': 'string',
                            'PerformanceInsightsRetentionPeriod': 123,
                            'EnabledCloudWatchLogsExports': [
                                'string',
                            ],
                            'ProcessorFeatures': [
                                {
                                    'Name': 'string',
                                    'Value': 'string'
                                },
                            ],
                            'ListenerEndpoint': {
                                'Address': 'string',
                                'Port': 123,
                                'HostedZoneId': 'string'
                            },
                            'MaxAllocatedStorage': 123
                        },
                        'AwsSnsTopic': {
                            'KmsMasterKeyId': 'string',
                            'Subscription': [
                                {
                                    'Endpoint': 'string',
                                    'Protocol': 'string'
                                },
                            ],
                            'TopicName': 'string',
                            'Owner': 'string'
                        },
                        'AwsSqsQueue': {
                            'KmsDataKeyReusePeriodSeconds': 123,
                            'KmsMasterKeyId': 'string',
                            'QueueName': 'string',
                            'DeadLetterTargetArn': 'string'
                        },
                        'AwsWafWebAcl': {
                            'Name': 'string',
                            'DefaultAction': 'string',
                            'Rules': [
                                {
                                    'Action': {
                                        'Type': 'string'
                                    },
                                    'ExcludedRules': [
                                        {
                                            'RuleId': 'string'
                                        },
                                    ],
                                    'OverrideAction': {
                                        'Type': 'string'
                                    },
                                    'Priority': 123,
                                    'RuleId': 'string',
                                    'Type': 'string'
                                },
                            ],
                            'WebAclId': 'string'
                        },
                        'AwsRdsDbSnapshot': {
                            'DbSnapshotIdentifier': 'string',
                            'DbInstanceIdentifier': 'string',
                            'SnapshotCreateTime': 'string',
                            'Engine': 'string',
                            'AllocatedStorage': 123,
                            'Status': 'string',
                            'Port': 123,
                            'AvailabilityZone': 'string',
                            'VpcId': 'string',
                            'InstanceCreateTime': 'string',
                            'MasterUsername': 'string',
                            'EngineVersion': 'string',
                            'LicenseModel': 'string',
                            'SnapshotType': 'string',
                            'Iops': 123,
                            'OptionGroupName': 'string',
                            'PercentProgress': 123,
                            'SourceRegion': 'string',
                            'SourceDbSnapshotIdentifier': 'string',
                            'StorageType': 'string',
                            'TdeCredentialArn': 'string',
                            'Encrypted': True|False,
                            'KmsKeyId': 'string',
                            'Timezone': 'string',
                            'IamDatabaseAuthenticationEnabled': True|False,
                            'ProcessorFeatures': [
                                {
                                    'Name': 'string',
                                    'Value': 'string'
                                },
                            ],
                            'DbiResourceId': 'string'
                        },
                        'AwsRdsDbClusterSnapshot': {
                            'AvailabilityZones': [
                                'string',
                            ],
                            'SnapshotCreateTime': 'string',
                            'Engine': 'string',
                            'AllocatedStorage': 123,
                            'Status': 'string',
                            'Port': 123,
                            'VpcId': 'string',
                            'ClusterCreateTime': 'string',
                            'MasterUsername': 'string',
                            'EngineVersion': 'string',
                            'LicenseModel': 'string',
                            'SnapshotType': 'string',
                            'PercentProgress': 123,
                            'StorageEncrypted': True|False,
                            'KmsKeyId': 'string',
                            'DbClusterIdentifier': 'string',
                            'DbClusterSnapshotIdentifier': 'string',
                            'IamDatabaseAuthenticationEnabled': True|False
                        },
                        'AwsRdsDbCluster': {
                            'AllocatedStorage': 123,
                            'AvailabilityZones': [
                                'string',
                            ],
                            'BackupRetentionPeriod': 123,
                            'DatabaseName': 'string',
                            'Status': 'string',
                            'Endpoint': 'string',
                            'ReaderEndpoint': 'string',
                            'CustomEndpoints': [
                                'string',
                            ],
                            'MultiAz': True|False,
                            'Engine': 'string',
                            'EngineVersion': 'string',
                            'Port': 123,
                            'MasterUsername': 'string',
                            'PreferredBackupWindow': 'string',
                            'PreferredMaintenanceWindow': 'string',
                            'ReadReplicaIdentifiers': [
                                'string',
                            ],
                            'VpcSecurityGroups': [
                                {
                                    'VpcSecurityGroupId': 'string',
                                    'Status': 'string'
                                },
                            ],
                            'HostedZoneId': 'string',
                            'StorageEncrypted': True|False,
                            'KmsKeyId': 'string',
                            'DbClusterResourceId': 'string',
                            'AssociatedRoles': [
                                {
                                    'RoleArn': 'string',
                                    'Status': 'string'
                                },
                            ],
                            'ClusterCreateTime': 'string',
                            'EnabledCloudWatchLogsExports': [
                                'string',
                            ],
                            'EngineMode': 'string',
                            'DeletionProtection': True|False,
                            'HttpEndpointEnabled': True|False,
                            'ActivityStreamStatus': 'string',
                            'CopyTagsToSnapshot': True|False,
                            'CrossAccountClone': True|False,
                            'DomainMemberships': [
                                {
                                    'Domain': 'string',
                                    'Status': 'string',
                                    'Fqdn': 'string',
                                    'IamRoleName': 'string'
                                },
                            ],
                            'DbClusterParameterGroup': 'string',
                            'DbSubnetGroup': 'string',
                            'DbClusterOptionGroupMemberships': [
                                {
                                    'DbClusterOptionGroupName': 'string',
                                    'Status': 'string'
                                },
                            ],
                            'DbClusterIdentifier': 'string',
                            'DbClusterMembers': [
                                {
                                    'IsClusterWriter': True|False,
                                    'PromotionTier': 123,
                                    'DbInstanceIdentifier': 'string',
                                    'DbClusterParameterGroupStatus': 'string'
                                },
                            ],
                            'IamDatabaseAuthenticationEnabled': True|False
                        },
                        'Container': {
                            'Name': 'string',
                            'ImageId': 'string',
                            'ImageName': 'string',
                            'LaunchedAt': 'string'
                        },
                        'Other': {
                            'string': 'string'
                        }
                    }
                },
            ],
            'Compliance': {
                'Status': 'PASSED'|'WARNING'|'FAILED'|'NOT_AVAILABLE',
                'RelatedRequirements': [
                    'string',
                ],
                'StatusReasons': [
                    {
                        'ReasonCode': 'string',
                        'Description': 'string'
                    },
                ]
            },
            'VerificationState': 'UNKNOWN'|'TRUE_POSITIVE'|'FALSE_POSITIVE'|'BENIGN_POSITIVE',
            'WorkflowState': 'NEW'|'ASSIGNED'|'IN_PROGRESS'|'DEFERRED'|'RESOLVED',
            'Workflow': {
                'Status': 'NEW'|'NOTIFIED'|'RESOLVED'|'SUPPRESSED'
            },
            'RecordState': 'ACTIVE'|'ARCHIVED',
            'RelatedFindings': [
                {
                    'ProductArn': 'string',
                    'Id': 'string'
                },
            ],
            'Note': {
                'Text': 'string',
                'UpdatedBy': 'string',
                'UpdatedAt': 'string'
            },
            'Vulnerabilities': [
                {
                    'Id': 'string',
                    'VulnerablePackages': [
                        {
                            'Name': 'string',
                            'Version': 'string',
                            'Epoch': 'string',
                            'Release': 'string',
                            'Architecture': 'string'
                        },
                    ],
                    'Cvss': [
                        {
                            'Version': 'string',
                            'BaseScore': 123.0,
                            'BaseVector': 'string'
                        },
                    ],
                    'RelatedVulnerabilities': [
                        'string',
                    ],
                    'Vendor': {
                        'Name': 'string',
                        'Url': 'string',
                        'VendorSeverity': 'string',
                        'VendorCreatedAt': 'string',
                        'VendorUpdatedAt': 'string'
                    },
                    'ReferenceUrls': [
                        'string',
                    ]
                },
            ]
        },
    ],
    'NextToken': 'string'
}




{
    "NextToken":"U2FsdGVkX1+mESPYuVpSc1qiOuPR4Cs1x747imDNbm3yfxqQORKxgJ0KaD/Cqmy87G1bcXtGZZRr0TafeFTOG8Vwe/qfizfW89rSTtUOm4opheiJN4BkTHMk2FSPbPGX02VgxnA+AmAzal92+osGoQLP7ppD6s6cV0aJWHFDC+0nNWbDMK6CQBxC9GWh/uchUEUjKTM2qIXr6UoV8Fwxz4vXOCP0ADaypQD0I0ZH0PGkvbp2SMFMkWExbXXGb7hsXFjftIpAmhNfdJmzujl/eT1n6ScLRsa93z0M0p1uxRzc27NcevE5PhOPY+ayRKXNnItqGO2KiAfKTrliRnjM5wkcQ8+o+xO6zhjCWqG7+bvbaa+GB40/ub/pVvDPqPHRPEIr5Yz4chBY3qRMZkj/+hQIYT/gKB8tP8U/Lr7cl0HcZS42GDl6Z2NKKWS4ujdntYyjOgtHS24w0ekfJtzNHw==",
    "Findings":[
       {
          "LastObservedAt":"2020-08-25T18:24:16.913Z",
          "FirstObservedAt":"2020-08-25T18:24:15.727Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/ELBv2.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"ELBv2.1 Application Load Balancer should be configured to redirect all HTTP requests to HTTPS",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/ELBv2.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-alb-http-to-https-redirection-check-b0e79d1c",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/ELBv2.1",
             "ControlId":"ELBv2.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/ELBv2.1/finding/fba93529-4f64-4269-be78-48201004463d",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:15.727Z",
          "UpdatedAt":"2020-08-25T18:24:15.727Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/ELBv2.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether HTTP to HTTPS redirection is configured on all HTTP listeners of Application Load Balancers. The control will fail if one or more HTTP listeners of Application Load Balancers do not have HTTP to HTTPS redirection configured.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/ELBv2.1/finding/fba93529-4f64-4269-be78-48201004463d",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:14.459Z",
          "FirstObservedAt":"2020-08-25T18:24:12.856Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/CodeBuild.2",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"CodeBuild.2 CodeBuild project environment variables should not contain clear text credentials",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/CodeBuild.2/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-codebuild-project-envvar-awscred-check-05b9772f",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/CodeBuild.2",
             "ControlId":"CodeBuild.2",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/CodeBuild.2/finding/4a596d95-8274-4d28-955b-7158fb6b6a4c",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:12.856Z",
          "UpdatedAt":"2020-08-25T18:24:12.856Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/CodeBuild.2/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the project contains environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/CodeBuild.2/finding/4a596d95-8274-4d28-955b-7158fb6b6a4c",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:13.089Z",
          "FirstObservedAt":"2020-08-25T18:24:11.731Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/SSM.2",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"SSM.2 EC2 instances managed by Systems Manager should have a patch compliance status of COMPLIANT after a patch installation",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/SSM.2/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-ec2-managedinstance-patch-compliance-47a8a309",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/SSM.2",
             "ControlId":"SSM.2",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SSM.2/finding/fa080c35-6cb9-4053-a8d6-484a1c19a640",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:11.731Z",
          "UpdatedAt":"2020-08-25T18:24:11.731Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/SSM.2/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the compliance status of the Amazon EC2 Systems Manager patch compliance is COMPLIANT or NON_COMPLIANT after the patch installation on the instance. It only checks instances that are managed by AWS Systems Manager Patch Manager.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SSM.2/finding/fa080c35-6cb9-4053-a8d6-484a1c19a640",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:11.824Z",
          "FirstObservedAt":"2020-08-25T18:24:10.226Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/SSM.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"SSM.1 EC2 instances should be managed by AWS Systems Manager",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/SSM.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-ec2-instance-managed-by-ssm-df8b5ff1",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/SSM.1",
             "ControlId":"SSM.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SSM.1/finding/26a762f5-6640-413e-bb2d-99460d20746b",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:10.226Z",
          "UpdatedAt":"2020-08-25T18:24:10.226Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/SSM.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the Amazon EC2 instances in your account are managed by AWS Systems Manager.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SSM.1/finding/26a762f5-6640-413e-bb2d-99460d20746b",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:12.260Z",
          "FirstObservedAt":"2020-08-25T18:24:09.961Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/EFS.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"EFS.1 Elastic File System should be configured to encrypt file data at-rest using AWS KMS",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/EFS.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-efs-encrypted-check-05cfec21",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/EFS.1",
             "ControlId":"EFS.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/EFS.1/finding/a15cbd15-10c0-486b-8817-f147f14b86d0",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:09.961Z",
          "UpdatedAt":"2020-08-25T18:24:09.961Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/EFS.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether Amazon Elastic File System (Amazon EFS) is configured to encrypt the file data using AWS Key Management Service (AWS KMS). The check will fail if the encrypted key is set to false on DescribeFileSystems or if the KmsKeyId key on DescribeFileSystems does not match the KmsKeyId parameter.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/EFS.1/finding/a15cbd15-10c0-486b-8817-f147f14b86d0",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:04.832Z",
          "FirstObservedAt":"2020-08-25T18:24:03.601Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/ACM.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"ACM.1 ACM certificates should be renewed after a specified time period",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/ACM.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-acm-certificate-expiration-check-097e99ec",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/ACM.1",
             "ControlId":"ACM.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/ACM.1/finding/82f69f54-4bd7-4cb3-8cfb-b4a2621abecf",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:03.601Z",
          "UpdatedAt":"2020-08-25T18:24:03.601Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/ACM.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether ACM Certificates in your account are marked for expiration within a specified time period. Certificates provided by ACM are automatically renewed. ACM does not automatically renew certificates that you import.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/ACM.1/finding/82f69f54-4bd7-4cb3-8cfb-b4a2621abecf",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:04.797Z",
          "FirstObservedAt":"2020-08-25T18:24:02.988Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/RDS.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"RDS.1 RDS snapshot should be private",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/RDS.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-rds-snapshots-public-prohibited-3b0f61b3",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/RDS.1",
             "ControlId":"RDS.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.1/finding/085eef45-990f-4d56-ac2c-ca030ec25e89",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:02.988Z",
          "UpdatedAt":"2020-08-25T18:24:02.988Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/RDS.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks if Amazon Relational Database Service (Amazon RDS) snapshots are public.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.1/finding/085eef45-990f-4d56-ac2c-ca030ec25e89",
          "Types":[
             "Effects/Data Exposure/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:24:02.240Z",
          "FirstObservedAt":"2020-08-25T18:24:00.863Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/S3.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"S3.1 S3 Block Public Access setting should be enabled",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/S3.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-s3-account-level-public-access-blocks-b5176ce0",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/S3.1",
             "ControlId":"S3.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/S3.1/finding/e63c84c6-8678-4264-9fb6-f68f2e4ac497",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:24:00.863Z",
          "UpdatedAt":"2020-08-25T18:24:00.863Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/S3.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the following public access block settings are configured from account level: ignorePublicAcls: True, blockPublicPolicy: True, blockPublicAcls: True, restrictPublicBuckets: True.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/S3.1/finding/e63c84c6-8678-4264-9fb6-f68f2e4ac497",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:59.775Z",
          "FirstObservedAt":"2020-08-25T18:23:57.778Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/CodeBuild.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"CodeBuild.1 CodeBuild GitHub or Bitbucket source repository URLs should use OAuth",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/CodeBuild.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-codebuild-project-source-repo-url-check-6ef4ea99",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/CodeBuild.1",
             "ControlId":"CodeBuild.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/CodeBuild.1/finding/24484e2f-19ef-410f-bed3-22ea88d9f962",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:57.778Z",
          "UpdatedAt":"2020-08-25T18:23:57.778Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/CodeBuild.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the GitHub or Bitbucket source repository URL contains either personal access tokens or user name and password.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/CodeBuild.1/finding/24484e2f-19ef-410f-bed3-22ea88d9f962",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:58.415Z",
          "FirstObservedAt":"2020-08-25T18:23:57.617Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/AutoScaling.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"AutoScaling.1 Auto scaling groups associated with a load balancer should use load balancer health checks",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/AutoScaling.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-autoscaling-group-elb-healthcheck-required-f424c4cf",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/AutoScaling.1",
             "ControlId":"AutoScaling.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/AutoScaling.1/finding/551ea38a-5afd-4144-b106-dba8d5e464af",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:57.617Z",
          "UpdatedAt":"2020-08-25T18:23:57.617Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/AutoScaling.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This control checks whether your Auto Scaling groups that are associated with a load balancer are using Elastic Load Balancing health checks.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/AutoScaling.1/finding/551ea38a-5afd-4144-b106-dba8d5e464af",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:58.418Z",
          "FirstObservedAt":"2020-08-25T18:23:57.489Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/SSM.3",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"SSM.3 EC2 instances managed by Systems Manager should have an association compliance status of COMPLIANT",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/SSM.3/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-ec2-managedinstance-association-compliance-status-check-8b1a09b1",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/SSM.3",
             "ControlId":"SSM.3",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SSM.3/finding/7baf5eb4-6386-4765-bb8d-4e1c1077a414",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:57.489Z",
          "UpdatedAt":"2020-08-25T18:23:57.489Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/SSM.3/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the status of the AWS Systems Manager association compliance is COMPLIANT or NON_COMPLIANT after the association is executed on an instance.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SSM.3/finding/7baf5eb4-6386-4765-bb8d-4e1c1077a414",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:56.896Z",
          "FirstObservedAt":"2020-08-25T18:23:55.223Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/RDS.3",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"RDS.3 RDS DB instances should have encryption at-rest enabled",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/RDS.3/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-rds-storage-encrypted-6c409f96",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/RDS.3",
             "ControlId":"RDS.3",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.3/finding/cadf57df-6095-4b72-b581-a0ab82e4803e",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:55.223Z",
          "UpdatedAt":"2020-08-25T18:23:55.223Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/RDS.3/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether storage encryption is enabled for your RDS DB instances.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.3/finding/cadf57df-6095-4b72-b581-a0ab82e4803e",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:55.879Z",
          "FirstObservedAt":"2020-08-25T18:23:54.780Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/EC2.3",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"EC2.3 Attached EBS volumes should be encrypted at-rest",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/EC2.3/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-encrypted-volumes-502fdd41",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/EC2.3",
             "ControlId":"EC2.3",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/EC2.3/finding/d67fb1af-6bc3-4433-a6a8-7a5703ca1f52",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:54.780Z",
          "UpdatedAt":"2020-08-25T18:23:54.780Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/EC2.3/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the EBS volumes that are in an attached state are encrypted.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/EC2.3/finding/d67fb1af-6bc3-4433-a6a8-7a5703ca1f52",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:55.079Z",
          "FirstObservedAt":"2020-08-25T18:23:53.511Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/CloudTrail.2",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"CloudTrail.2 CloudTrail should have encryption at-rest enabled",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/CloudTrail.2/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-cloud-trail-encryption-enabled-oqc2de",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/CloudTrail.2",
             "ControlId":"CloudTrail.2",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/CloudTrail.2/finding/1507f6ea-ac2b-4768-9223-05f4fc52d1f9",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:53.511Z",
          "UpdatedAt":"2020-08-25T18:23:53.511Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/CloudTrail.2/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether AWS CloudTrail is configured to use the server side encryption (SSE) AWS Key Management Service (AWS KMS) customer master key (CMK) encryption. The check will pass if the KmsKeyId is defined.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/CloudTrail.2/finding/1507f6ea-ac2b-4768-9223-05f4fc52d1f9",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:52.735Z",
          "FirstObservedAt":"2020-08-25T18:23:51.889Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/SageMaker.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"SageMaker.1 Amazon SageMaker notebook instances should not have direct internet access",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/SageMaker.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-sagemaker-notebook-no-direct-internet-access-a0945d13",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/SageMaker.1",
             "ControlId":"SageMaker.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SageMaker.1/finding/96673cb1-2a8c-43cd-9220-b35c29ebe9b8",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:51.889Z",
          "UpdatedAt":"2020-08-25T18:23:51.889Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/SageMaker.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether direct internet access is disabled for an Amazon SageMaker notebook instance by examining the DirectInternetAccess field is disabled for an Amazon SageMaker notebook instance.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/SageMaker.1/finding/96673cb1-2a8c-43cd-9220-b35c29ebe9b8",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:53.041Z",
          "FirstObservedAt":"2020-08-25T18:23:51.267Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/EC2.4",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"EC2.4 Stopped EC2 instances should be removed after a specified time period",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/EC2.4/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-ec2-stopped-instance-bcfe8941",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/EC2.4",
             "ControlId":"EC2.4",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/EC2.4/finding/fd4cfeef-06b5-49be-b4c7-d9e7975412dd",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:51.267Z",
          "UpdatedAt":"2020-08-25T18:23:51.267Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/EC2.4/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This control checks whether any EC2 instances have been stopped for more than the allowed number of days. An EC2 instance fails this check if it is stopped for longer than the maximum allowed time period, which by default is 30 days.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/EC2.4/finding/fd4cfeef-06b5-49be-b4c7-d9e7975412dd",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:47.427Z",
          "FirstObservedAt":"2020-08-25T18:23:45.763Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/DMS.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"DMS.1 Database Migration Service replication instances should not be public",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/DMS.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-dms-replication-not-public-d40af75c",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/DMS.1",
             "ControlId":"DMS.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/DMS.1/finding/8b3739dd-8bf0-4052-80a5-5825f7474847",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:45.763Z",
          "UpdatedAt":"2020-08-25T18:23:45.763Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/DMS.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether AWS Database Migration Service replication instances are public by examining the PubliclyAccessible field value.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/DMS.1/finding/8b3739dd-8bf0-4052-80a5-5825f7474847",
          "Types":[
             "Effects/Data Exposure/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:33.755Z",
          "FirstObservedAt":"2020-08-25T18:23:32.016Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/RDS.2",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"RDS.2 RDS DB Instances should prohibit public access, determined by the PubliclyAccessible configuration",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/RDS.2/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-rds-instance-public-access-check-0b9f5d39",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/RDS.2",
             "ControlId":"RDS.2",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.2/finding/021253fd-7782-4244-86b7-e3e69b736181",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:32.016Z",
          "UpdatedAt":"2020-08-25T18:23:32.016Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/RDS.2/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether RDS instances are publicly accessible by evaluating the publiclyAccessible field in the instance configuration item.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/RDS.2/finding/021253fd-7782-4244-86b7-e3e69b736181",
          "Types":[
             "Effects/Data Exposure/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:23:31.746Z",
          "FirstObservedAt":"2020-08-25T18:23:31.263Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/ES.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"ES.1 ElasticSearch domains should have encryption at-rest enabled",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED",
             "StatusReasons":[
                {
                   "ReasonCode":"CONFIG_EVALUATIONS_EMPTY",
                   "Description":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
                }
             ]
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/ES.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "RelatedAWSResources:0/name":"securityhub-elasticsearch-encrypted-at-rest-a17c5d6a",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/ES.1",
             "ControlId":"ES.1",
             "RelatedAWSResources:0/type":"AWS::Config::ConfigRule",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/ES.1/finding/6932221f-28d5-4178-acfb-f71a59a793a5",
             "aws/securityhub/CompanyName":"AWS",
             "aws/securityhub/annotation":"AWS Config evaluated your resources against the rule. The rule did not apply to the AWS resources in its scope, the specified resources were deleted, or the evaluation results were deleted."
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:23:31.263Z",
          "UpdatedAt":"2020-08-25T18:23:31.263Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/ES.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether Amazon Elasticsearch Service (Amazon ES) domains have encryption at rest configuration enabled. This check will fail if the EncryptionAtRestOptions field is not enabled.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/ES.1/finding/6932221f-28d5-4178-acfb-f71a59a793a5",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       },
       {
          "LastObservedAt":"2020-08-25T18:12:10.255Z",
          "FirstObservedAt":"2020-08-25T18:12:08.242Z",
          "GeneratorId":"aws-foundational-security-best-practices/v/1.0.0/Config.1",
          "Severity":{
             "Product":0,
             "Normalized":0,
             "Original":"INFORMATIONAL",
             "Label":"INFORMATIONAL"
          },
          "Workflow":{
             "Status":"RESOLVED"
          },
          "Title":"Config.1 AWS Config should be enabled",
          "Resources":[
             {
                "Region":"us-east-1",
                "Partition":"aws",
                "Type":"AwsAccount",
                "Id":"AWS::::Account:883289105955"
             }
          ],
          "Compliance":{
             "Status":"PASSED"
          },
          "ProductArn":"arn:aws:securityhub:us-east-1::product/aws/securityhub",
          "ProductFields":{
             "StandardsArn":"arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
             "RecommendationUrl":"https://docs.aws.amazon.com/console/securityhub/Config.1/remediation",
             "StandardsSubscriptionArn":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0",
             "StandardsControlArn":"arn:aws:securityhub:us-east-1:883289105955:control/aws-foundational-security-best-practices/v/1.0.0/Config.1",
             "ControlId":"Config.1",
             "aws/securityhub/ProductName":"Security Hub",
             "aws/securityhub/FindingId":"arn:aws:securityhub:us-east-1::product/aws/securityhub/arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/Config.1/finding/0ed6de76-3296-4b46-b347-900aa8ebf198",
             "aws/securityhub/CompanyName":"AWS"
          },
          "RecordState":"ACTIVE",
          "WorkflowState":"NEW",
          "CreatedAt":"2020-08-25T18:12:08.242Z",
          "UpdatedAt":"2020-08-25T18:12:08.242Z",
          "Remediation":{
             "Recommendation":{
                "Url":"https://docs.aws.amazon.com/console/securityhub/Config.1/remediation",
                "Text":"For directions on how to fix this issue, please consult the AWS Security Hub Foundational Security Best Practices documentation."
             }
          },
          "Description":"This AWS control checks whether the Config service is enabled in the account for the local region and is recording all resources.",
          "SchemaVersion":"2018-10-08",
          "Id":"arn:aws:securityhub:us-east-1:883289105955:subscription/aws-foundational-security-best-practices/v/1.0.0/Config.1/finding/0ed6de76-3296-4b46-b347-900aa8ebf198",
          "Types":[
             "Software and Configuration Checks/Industry and Regulatory Standards/AWS-Foundational-Security-Best-Practices"
          ],
          "AwsAccountId":"883289105955"
       }
    ],
    "ResponseMetadata":{
       "RetryAttempts":0,
       "HTTPStatusCode":200,
       "RequestId":"deca0bb6-49d9-44fc-98e0-898b5c38edbf",
       "HTTPHeaders":{
          "x-amzn-requestid":"deca0bb6-49d9-44fc-98e0-898b5c38edbf",
          "content-length":"58586",
          "x-amz-apigw-id":"R1vIIFBaoAMFZJQ=",
          "x-amzn-trace-id":"Root=1-5f455f00-9cd800e40e901bc4c622cbd6;Sampled=0",
          "connection":"keep-alive",
          "date":"Tue, 25 Aug 2020 18:57:04 GMT",
          "content-type":"application/json"
       }
    }
 }