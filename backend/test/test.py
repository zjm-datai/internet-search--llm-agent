from vllm import LLM, SamplingParams

def testVllm(model_path: str):
    llm = LLM(
        model=model_path, 
        tensor_parallel_size=1, # 如果只在一张卡上跑就设置为 1
        gpu_memory_utilization=0.9,
        dtype="auto",
        max_model_len=4096,
        enforce_eager=True,
        # device="cuda:6",    
    )

    sampling_params = SamplingParams(temperature=0.7, top_p=0.9, max_tokens=100)

    # 运行推理
    outputs = llm.generate(
        ["你好，请介绍一下你自己。"],
        sampling_params
    )

    # 输出结果
    for output in outputs:
        print(output.outputs[0].text)

def testTransformer(model_path: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)

if __name__ == "__main__":
    model_path = "../models/Qwen2.5-1.5B-Instruct"

    testVllm(model_path)
