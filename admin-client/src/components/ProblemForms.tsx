import { useState } from 'react'
import axios from 'axios';

interface ProblemFormsProps {
  endpoint: string
}

interface ProblemFormProps extends ProblemFormsProps {
  seq: number
  form_id: number
}

function ProblemForm ({ endpoint, seq, form_id }: ProblemFormProps) {
  const [formData, setFormData] = useState({
    problem_url: '',
    problem_number: null,
    topic: ''
  })

  const [message, setMessage] = useState('')


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value
    })
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const body = {
        ...formData,
        seq,
        form_id
      }
      console.log('Post request body:', body);
      const response = await axios.post(endpoint, body);
      setMessage(response.data.message)
      // Optionally handle success
    } catch (error) {
      console.error('Error submitting form:', error)
      // Optionally handle error
    }
  }

  return (
    <div>
      {message !== '' && <div>{message}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type='text'
          name='problem_url'
          placeholder='Problem URL'
          value={formData.problem_url}
          onChange={handleChange}
        />
        <input
          type='number'
          name='problem_number'
          placeholder='Problem Number'
          value={formData.problem_number || ''}
          onChange={handleChange}
        />
        <input
          type='text'
          name='topic'
          placeholder='Topic'
          value={formData.topic}
          onChange={handleChange}
        />
        <br />
        <button type='submit'>Submit</button>
      </form>
    </div>
  )
}


export default function ProblemForms({ endpoint }: ProblemFormsProps) {

  const [formId, setFormId] = useState<number | null>(null)


  return (
    <div>

      <div className="form-id-selector">
        <label>
          Form ID:
          <input
            type='number'
            value={formId || ''}
            onChange={e => setFormId(parseInt(e.target.value))}
          />
        </label>
      </div>

      <h1>Problem 1</h1>
      <ProblemForm
        endpoint={endpoint}
        seq={0}
        form_id={formId || 0}
      />
      <h1>Problem 2</h1>
      <ProblemForm
        endpoint={endpoint}
        seq={1}
        form_id={formId || 0}
      />
    </div>
  )
}
