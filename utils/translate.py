#将前端传输的数据进行翻译: "attempt_match" -> "intents",读取"input_content"、"output_content"里的内容
import re
def translate(data_:dict):
    data=data_
    nameMap = data["nameMap"]
    for task in data_["tasks"].values():

        # name -> id
        task["name"] = task["id"]

        #inputs
        package_=task["input_content"]["data"]
        # print("input_content: ",package_)
        input_content_=None
        if "input_content" in package_:
            input_content_=package_["input_content"]
            del package_["input_content"]
        inputs=list()
        for key in package_.keys():
            inputs.append(key)

            
        del task["input_content"]

        if input_content_ is not None:

            matches = re.findall(r"\{(.*?)\}",input_content_)
            print(1,matches)
            for match in matches:
                trans = name_translate(nameMap,match)
                input_content_ = input_content_.replace(match,trans)

            task.update({"input_content":input_content_})

        # 移除reason,output等无关的
        for toremove in ["output","reason"]:
            if toremove in inputs:
                inputs.remove(toremove)
        task["inputs"]=inputs

        #outputs
        if "output_content" in task:
            package_=(task["output_content"]["data"])
            # print("output_content: ",package_)
            output_content_=None
            if "output_content" in package_:
                output_content_=package_["output_content"]
                del package_["output_content"]
            outputs=list()
            for key in package_.keys():
                outputs.append(key)


            del task["output_content"]

        if output_content_ is not None:

            matches = re.findall(r"\{(.*?)\}",output_content_)
            print(2,matches)
            for match in matches:
                trans = name_translate(nameMap,match)
                output_content_ = output_content_.replace(match,trans)

            task.update({"output_content":output_content_})
        
        for toremove in ["output","reason"]:
            if toremove in outputs:
                outputs.remove(toremove)

        task["outputs"]=outputs

        if "attempt_match" in task:
            intents = task["attempt_match"]["data"]
            del task["attempt_match"]
            task.update({"intents":intents})
        
    return data

def detranslate(data_:dict):
    data=data_
    for task in data["tasks"].values():
        #inputs
        input_content_=dict()
        for input in task["inputs"]:
            input_content_.update({input:""})
        if "input_content" in task:
            input_content_.update({"input_content":task["input_content"]})
        #outputs
        output_content_=dict()
        for output in task["outputs"]:
            output_content_.update({output:""})
        if "output_content" in task:
            output_content_.update({"output_content":task["output_content"]})
        for key in ["inputs","outputs","input_content","output_content"]:
            if key in task:
                del task[key]
        task.update({"input_content":input_content_})
        task.update({"output_content":output_content_})

        #branch
        if "intents" in task:
            intents = task["intents"]
            del task["intents"]
            task["attempt_match"]=intents
    return data
        


def name_translate(nameMap,name:str):
    '''
    给出一个映射表,将变量名改成名字_output或名字_input,并去掉“.”
    '''
    name = name.split(".")
    name_ch = name[0]
    name[1]="_output"
    if name_ch not in nameMap:
        print(f"fail to map name{name_ch}")
        return None

    name_mapped = nameMap[name_ch]
    name[0] = name_mapped
    return str("".join(name))
