import { useState, useEffect } from "react"


export const App = () => {
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(false)
  const [res, setRes] = useState(null)
  useEffect(() => {
    if (!res) {
      setProcessing(true); setError(false)
      fetch("https://yappiest-carina-krik8235-ffe52731.koyeb.app/browse", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
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
          console.log(res, res)
          setRes(res)
          if (res?.ok === false) { setProcessing(false); setError(true) }
          else setProcessing(false)
        })
        .catch(err => { console.log(err); setRes(err); setProcessing(false); setError(true); })
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
