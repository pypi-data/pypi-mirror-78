from __future__ import print_function
import sys
import os
import logging
import json
import copy
from os.path import dirname
from jsonschema import validate
import importlib
import pkgutil
import tempfile
import uuid
from halocli.exception import HaloPluginException
from halocli.util import Util

logger = logging.getLogger(__name__)

logging.root.setLevel(logging.INFO)

"""
the bian plugin
---------------

1. no segregation and add id for no segregation items - done

2. add proprietary bank fields from legacy - done

3. add mappings from legacy to bian fields

4. generate collection-filter parameter list

5. add sub BQ as needed

6. add new endpoints as needed

7. refactor bian types in specific fields where type is generic(string, etc..)

8. add version metadata for control and traceability

"""

class Plugin():

    def __init__(self,halo):
        #init vars
        self.halo = halo

        #init work on halo config
        #if self.halo.config ...

        self.name = 'extend'
        self.desc = 'extend bian swagger file'

        # set commands
        self.commands = {
            'testy': {
                'usage': "test this for your HALO project",
                'lifecycleEvents': ['resources', 'functions']
            },
            'method1': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'before:method1:generate': self.before_method_generate,
            'method1:generate': self.method_generate,
            'after:method1:generate': self.after_method_generate,
            'method1:write': self.method_write,
        }

        #logger.info('finished plugin')

    def run_plugin(self,options):
        self.options = options
        #do more

    def before_method_generate(self):
        service = None
        path = None
        if hasattr(self, 'options'):
            if self.options:
                for o in self.options:
                    if 'service' in o:
                        service = o['service']
                    if 'path' in o:
                        path = o['path']
        if not service:
            raise Exception("no service found")
        self.service = service
        urls = self.halo.settings['mservices'][service]['record']['path']
        self.path = path
        self.data = Util.analyze_swagger(urls)


    def method_generate(self):
        data = self.data
        tmp = {}
        bqs = []
        for d in data['paths']:
            # {'get': {
            # 'tags': ['retrieve'],
            # 'summary': 'Analytical views maintained by the SDCurrentAccount service center for management reporting and analysis purposes',
            # 'description': 'Analytical views maintained by the SDCurrentAccount service center for management reporting and analysis purposes',
            # 'operationId': 'retrieveSDCurrentAccount',
            # 'produces': ['application/json'],
            # 'parameters': [{'name': 'sd-reference-id', 'in': 'path', 'description': 'SDCurrentAccount Servicing Session Reference', 'required': True, 'type': 'string'}, {'name': 'queryparams', 'in': 'query', 'description': "Query params from schema '#/definitions/SDCurrentAccountRetrieveInputModel'", 'required': False, 'type': 'string'}],
            # 'responses': {'200': {'description': 'Successful Service Retrieve', 'schema': {'type': 'object', 'properties': {'serviceDomainRetrieveActionTaskReference': {'type': 'string', 'example': 'SRATR795161', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::ISO20022andUNCEFACT::Identifier\n general-info: Reference to a retrieve service call\n'}, 'serviceDomainRetrieveActionTaskRecord': {'type': 'object', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Binary\n general-info: The retrieve service call consolidated processing record\n', 'properties': {}}, 'serviceDomainRetrieveActionResponse': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Details of the retrieve action service response (lists returned reports)\n'}, 'serviceDomainRetrieveActionRecord': {'properties': {'serviceDomainActivityAnalysis': {'properties': {'activityAnalysisReference': {'type': 'string', 'example': '730230', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::ISO20022andUNCEFACT::Identifier\n general-info: Reference to the internal activity analysis view maintained by the service center\n'}, 'activityAnalysisResult': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: The results of the activity analysis that can be on-going, periodic and actual and projected\n'}, 'activityAnalysisReportType': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Code\n general-info: The type of activity analysis report available\n'}, 'activityAnalysisReport': {'type': 'object', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Binary\n general-info: The activity analysis report in any suitable form including selection filters where appropriate\n', 'properties': {}}}}, 'serviceDomainPerformanceAnalysis': {'properties': {'performanceAnalysisReference': {'type': 'string', 'example': '761670', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::ISO20022andUNCEFACT::Identifier\n general-info: Reference to the internal performance analysis view maintained by the service center\n'}, 'performanceAnalysisResult': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: The results of the performance analysis that can be on-going or periodic\n'}, 'performanceAnalysisReportType': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Code\n general-info: The type of performance analysis report available\n'}, 'performanceAnalysisReport': {'type': 'object', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Binary\n general-info: The performance analysis report in any suitable form including selection filters where appropriate\n', 'properties': {}}}}, 'controlRecordPortfolioAnalysis': {'properties': {'controlRecordPortfolioAnalysisReference': {'type': 'string', 'example': '739764', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::ISO20022andUNCEFACT::Identifier\n general-info: Reference to the control record portfolio analysis view maintained by the service center\n'}, 'controlRecordPortfolioAnalysisResult': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: The results of the portfolio analysis that can be on-going, periodic and actual and projected (can be unstructured data)\n'}, 'controlRecordPortfolioAnalysisReportType': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Code\n general-info: The type of external portfolio analysis report available\n'}, 'controlRecordAnalysisReport': {'type': 'object', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Binary\n general-info: The external analysis report in any suitable form including selection filters where appropriate\n', 'properties': {}}}}}}, 'serviceDomainOfferedService': {'properties': {'serviceDomainServiceReference': {'type': 'string', 'example': '776158', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::ISO20022andUNCEFACT::Identifier\n general-info: Reference to a service offered by the service center\n'}, 'serviceDomainServiceRecord': {'properties': {'serviceDomainServiceType': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Refers to the different types of services offered\n'}, 'serviceDomainServiceVersion': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: The version details of the service when appropriate\n'}, 'serviceDomainServiceDescription': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Description of the offered service \n'}, 'serviceDomainServicePoliciesandGuidelines': {'properties': {'serviceDomainServiceEligibility': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Policies and rules governing access to the offered service, includes eligibility and qualifications\n'}, 'serviceDomainServiceIntendedUses': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Guidelines covering allowed, intended use of the service\n'}, 'serviceDomainServicePricingandTerms': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Terms, prices, penalties associated with use of the service\n'}}}, 'serviceDomainServiceSchedule': {'type': 'string', 'description': '`status: Not Mapped`\n core-data-type-reference: BIAN::DataTypesLibrary::CoreDataTypes::UNCEFACT::Text\n general-info: Schedule defining when the accessed service is available\n'}}}}}}}}}}}
            m = data['paths'][d]
            if 'get' in m:
                # /current-account/{sd-reference-id}/current-account-fulfillment-arrangement/{cr-reference-id}/interest/{bq-reference-id}/
                if d.endswith("/behavior-qualifiers/"):
                    logger.debug("bqs:" + str(m))
                    bqs = m['get']['responses']['200']['schema']['example']
                if 'ReferenceIdsExtend' in m['get']['operationId']:
                    new_m = copy.deepcopy(m)
                    tmp[d] = new_m
        # fix the response and add
        for k in tmp:
            # bq methods
            ref_m = tmp[k]
            new_m = copy.deepcopy(ref_m)
            props = new_m['get']['responses']['200']['schema']['items']['properties']
            for p in props:
                if "methods" in self.halo.settings['mservices'][self.service]['record']:
                    for mthd in self.halo.settings['mservices'][self.service]['record']['methods']:
                        if mthd == new_m['get']['operationId']:
                            for target in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields']:
                                if p.endswith(target):
                                    self.halo.cli.log(new_m['get']['operationId'])
                                    #props[p]['properties']["ObjectReference"] = {"type":"string"}
                                    for fld in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields'][target]:
                                        type = self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields'][target][fld]
                                        props[p]['properties'][fld] = {"type": type}
            data['paths'][k] = new_m


        self.halo.cli.log("finished extend seccessfuly")

    def after_method_generate(self):
        data = self.data
        Util.validate_swagger(data)

    def method_write(self):
        try:
            path = self.path
            if path:
                file_path = os.path.join(path, str(uuid.uuid4()) + ".json")
            else:
                dir_tmp = tempfile.TemporaryDirectory()
                file_path = os.path.join(dir_tmp.name, str(uuid.uuid4()) + ".json")
            logger.debug(file_path)
            f = open(file_path, "a")
            f.write("")
            f.close()
            Util.dump_file(file_path, self.data)
            logging.debug("Swagger file generated:" + file_path)
            """
            with open(file_path, 'r') as fi:
                f = fi.read()
                print(str(f))
                return f
            """
            return 0
        except Exception as e:
            raise HaloPluginException(str(e))




