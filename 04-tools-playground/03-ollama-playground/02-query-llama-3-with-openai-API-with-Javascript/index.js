import OpenAI from 'openai'

const openai = new OpenAI({
  baseURL: 'http://localhost:11434/v1/',

  // required but ignored
  apiKey: 'ollama',
})

const completion = await openai.chat.completions.create({
  messages: [{ role: 'user', content: 'Say this is a test' }],
  model: 'llama3',
})

console.log(completion.choices[0].message)
