import axios from 'axios'
import { useEffect, useState } from 'react'

interface ServerMonitorProps {
  endpoint: string
}

export default function ServerMonitor ({ endpoint }: ServerMonitorProps) {
  const [status, setStatus] = useState<string>('')
  const [tickSeconds, setTickSeconds] = useState<number>(5)
  useEffect(() => {
    async function fetchStatus () {
      try {
        const response = await axios.get(endpoint)
        setStatus(response.data.status)
        console.log(new Date().getTime())
      } catch (error) {
        console.error('Error fetching server status:', error)
        setStatus('Error fetching server status')
      }
    }

    fetchStatus()

    const interval = setInterval(() => {
      fetchStatus()
    }, tickSeconds * 1000)

    return () => clearInterval(interval)
  }, [endpoint, tickSeconds])

  return (
    <div>
      <h2>Server Monitor</h2>
      <h3>Status: {status}</h3>
      <label htmlFor='tickSeconds'>
        Tick Seconds:
        <input
          type='number'
          value={tickSeconds}
          onChange={e => setTickSeconds(parseInt(e.target.value))}
        />
      </label>
    </div>
  )
}
