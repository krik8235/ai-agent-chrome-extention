import { useState, useEffect } from "react"


export const App = () => {
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(false)
  const [res, setRes] = useState(null)
  useEffect(() => {
    const asyncFetch = async () => {
      setProcessing(true); setError(false)
      await fetch("https://api-ai-chrome.koyeb.app/browse", {
        method: "POST",
        mode: "cors",
        headers: {
          "Origin": "https://rag-agent-system-chrome-extention.vercel.app",
          "Access-Control-Request-Method": "POST, OPTIONS",
          "Access-Control-Request-Headers": "*",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(
          {
            "request": "discount",
            "listings": [
              {
                "name": "Upright Piano",
                "description": "Beautiful upright piano in great condition",
                "value": 1000
              }
            ]
          }
        ),
      })
        .then(res => {
          setRes(res)
          if (res?.ok === false) { setProcessing(false); setError(true) }
          else setProcessing(false)
        })
        .catch(err => { console.log(err); setRes("error"); setProcessing(false); setError(true); })
    }
    if (res === null) {
      asyncFetch()
    }
  }, [res])


  return (
    <div className="container content section">
      <h1>Test API connection</h1>
      {processing && <p>Processing</p>}
      {error && <p>Something went wrong.</p>}
      {(res && !error) && <p> Successfully connected 🤠</p>}
    </div >
  )
}
