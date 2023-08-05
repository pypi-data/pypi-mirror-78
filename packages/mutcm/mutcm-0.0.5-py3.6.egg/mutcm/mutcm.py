import os, json, requests

class TCMParser:
    def __init__(self, case_dir):
        self.components = {}
        self.cases = []
        self.case_runs = []
        self.case_dir = case_dir
        self.parse(case_dir)

    def api_test(self, x):
        res = requests.request(x['method'], url=x['url'])
        print(res.status_code)
        return res.status_code

    def parse(self, case_dir):
        self.case_dir = case_dir
        self.case_folder = self.case_dir
        print(self.case_dir)
        f = []
        self.runs = []
        for (root,dirs,files) in os.walk(self.case_dir, topdown=True):
            print("Root => {}".format(root))
            # print(dirs)
            # print(files)
            # for dir in dirs:
            for case_file in files:
                process =  root.split('/')[2]
                project = root.split('/')[1]
                case = {}
                case['id'] = "{}-{}-{}".format(project,process,case_file.split(' ')[0])
                case['project'] = project
                case['process'] = process
                case['title'] = case_file
                case_file = os.path.join(root, case_file)
                case['data'] = (self.parse_single_file(case_file))
                self.cases.append(case)
        print("=================")
        print(self.cases)
        return self.cases

    def parse_single_file(self, case_file):
        print(case_file)
        f = open(case_file, "r")
        current_component = None
        current_text = ""
        test_method = ""
        seviarity = ""
        is_code = False
        code = ''
        codes = {}
        for x in f:
            if x.startswith('## ') and not is_code:
                current_component = x.split('## ')[1].strip()
                current_text = ""
            elif x.startswith('--') and current_component != None and not is_code:
                self.components[current_component] = current_text.strip()
            elif x.startswith('# ') and not is_code:
                test_method = x.split('# ')[1]
                self.components['test_method'] = test_method.strip()
            elif x.startswith('~') and not is_code:
                seviarity = x.split('~')[1]
                self.components['seviarity'] = seviarity.strip()
            elif x.startswith('```'):
                print("Code begin")
                if not is_code:
                    current_code = x.split('```')[1].strip()
                    is_code = True
                else:
                    codes[current_code] = code
                    is_code = False
                    current_text = (code)
                    code = ''
            elif is_code:
                code = code + x
            elif current_component not in ['', None] and not is_code:
                current_text = current_text + x.strip() + '\n'


        for comp in self.components:
            if 'Scenarios' in comp:
                print("Secnario found => {}".format(self.components[comp]))
                self.scenario = self.components[comp]
            elif 'Steps' in comp:
                print("Steps found => {}".format(self.components[comp]))
                self.steps = self.components[comp]

        scenario_text = {}

        self.scenario = json.loads(self.scenario)
        self.final_steps = []
        for scenario in self.scenario:
            current_step = self.steps
            for sce in self.scenario[scenario]:
                if sce.startswith('text'):
                    scenario_text['scenario_{}'.format(sce)] = self.scenario[scenario][sce]
                    find = '<scenario_{}>'.format(sce)
                    replace = str(self.scenario[scenario][sce])
                    current_step = current_step.replace(find,replace)
            print("xxxx")
            current_step = current_step.replace("'", '"')
            print(current_step)
            current_step_json = json.loads(current_step)
            current_step_json['expected'] = self.scenario[scenario]['expected']
            current_step_json['scenario'] = self.scenario[scenario]['scenario']
            print("xxxx")
            self.final_steps.append(current_step_json)
            self.case_runs.append(current_step_json)
        print('=======')
        # print(scenario_text)





        # for st in scenario_text:
        #     tt = scenario_text[st]
        #     rep_tt = '<{}>'.format(st)
        #     self.final_steps = self.final_steps.replace(rep_tt, tt)
        # # self.steps = json.load(self.steps)
        print((self.final_steps))
        self.components['Steps'] = self.final_steps

        self.components['Scenarios'] = json.loads(self.components['Scenarios'])

        return(self.components)
