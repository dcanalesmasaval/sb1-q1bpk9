import React, { useState } from 'react'
import { Send } from 'lucide-react'

function App() {
  const [message, setMessage] = useState('')
  const [conversation, setConversation] = useState<Array<{ role: string; content: string }>>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    setIsLoading(true)
    setConversation(prev => [...prev, { role: 'user', content: message }])
    setMessage('')

    try {
      const response = await fetch('/send_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'user1', // In a real app, this would be a unique user ID
          message: message,
        }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      setConversation(prev => [...prev, { role: 'assistant', content: data.message }])
    } catch (error) {
      console.error('Error:', error)
      setConversation(prev => [...prev, { role: 'assistant', content: 'Sorry, there was an error processing your request.' }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">AI Assistant Chat</h1>
      </header>
      <main className="flex-grow overflow-auto p-4">
        <div className="max-w-3xl mx-auto space-y-4">
          {conversation.map((msg, index) => (
            <div key={index} className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-white'} max-w-sm`}>
              {msg.content}
            </div>
          ))}
        </div>
      </main>
      <footer className="p-4 bg-white border-t">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-grow p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white p-2 rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            {isLoading ? 'Sending...' : <Send size={24} />}
          </button>
        </form>
      </footer>
    </div>
  )
}

export default App