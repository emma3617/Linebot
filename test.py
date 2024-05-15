from openai import OpenAI
import httpx

client2 = OpenAI(
    base_url="https://api.xty.app/v1", 
    api_key="sk-3ChT0jo7yOfOGbVMB58017E038Bf40Bb819d4e608dE28eB7",
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

completion = client2.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你好啊!"}
  ]
)

print(completion)