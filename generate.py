import g4f
import pandas as pd
import time
# from datasets import load_dataset, DatasetDict

# normal response
def paraphrase(text):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": text}],
    )  # alterative model setting


    return response

# def load_data():
#     dataset = load_dataset("text", data_files='./data/train.txt')
#     dataset = dataset['train'].shuffle(seed=42).select(range(100000,320000))
#     dataset = DatasetDict({
#                 'train': dataset
#             })
#     return dataset

def main():
    dataset = pd.read_csv('/home/link/spaces/gpt4free_2/benchmark/benchmark.csv')
    dataset = dataset.iloc[502:, :]
    queries = dataset["Query"].tolist()
    results = dataset["Result"].tolist()
    results = [eval(result)[0] for result in results]

    for i in range(len(queries)):
        print("=======================================")
        print("query:", queries[i])
        print("=======================================")
        print("Result:", results[i])

        # prompt = f"""Sinh cho tôi 3 câu tiếng việt có ý nghĩa tương tự với hai câu sau: "{queries[i]}" và ""{results[i]} """
        prompt = f""" Sinh cho tôi 3 câu hỏi tiếng việt có ý nghĩa tương tự với câu sau, lưu ý phải khác nhau về mặt từ vựng và cấu trúc nhiều hơn 50%, mỗi câu sinh ra trên một dòng, không đánh số thứ tự: " {results[i]}  """

        try:
            
            response = paraphrase(prompt)
            response = response.replace("\n", " ;")
            
            try_count = 0
            while any(keyword in response for keyword in ["IP","Email", "html", "167.", "page", "HTTP"]):
                response = paraphrase(prompt)
                try_count +=1
                print("Toang")
                if try_count == 5:
                    break

            if try_count == 5:
                continue

            print("=======================================")
            print("Response: ", response)
            print("=======================================")

            with open('benchmark3.csv','a') as fd:
                fd.write(f'\n"{queries[i]}","{results[i]}","{response}"')
            time.sleep(5)

        except Exception as e:
            print("Error: ", e)
            time.sleep(1)

if __name__ == '__main__':
    main()