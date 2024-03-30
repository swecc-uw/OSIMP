import React, { useState } from 'react';
import axios from 'axios'; // Make sure to install axios: npm install axios

interface TestEmailFormProps {
  endpoint: string;
}

const TestEmailForm = ({ endpoint }: TestEmailFormProps) => {
  const [formData, setFormData] = useState({
    paired_content: '',
    unpaired_content: '',
    paired_subject: '',
    unpaired_subject: '',
    resend: false,
    email_unpaired: 'elimelt@uw.edu',
    email_paired: 'elimelt@uw.edu'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await axios.post(endpoint, formData);
      console.log('Post request response:', response.data);
      // Optionally handle success
    } catch (error) {
      console.error('Error submitting form:', error);
      // Optionally handle error
    }
  };

  return (
    <div>
      <textarea
        name="paired_content"
        placeholder="Paired Content"
        value={formData.paired_content}
        onChange={handleChange}
      />
      <br />
      <textarea
        name="unpaired_content"
        placeholder="Unpaired Content"
        value={formData.unpaired_content}
        onChange={handleChange}
      />
      <form onSubmit={handleSubmit}>

        <input
          type="text"
          name="paired_subject"
          placeholder="Paired Subject"
          value={formData.paired_subject}
          onChange={handleChange}
        />
        <br />
        <input
          type="text"
          name="unpaired_subject"
          placeholder="Unpaired Subject"
          value={formData.unpaired_subject}
          onChange={handleChange}
        />
        <br />
        <input
          type="text"
          name="email_unpaired"
          placeholder="Email Unpaired"
          value={formData.email_unpaired}
          onChange={handleChange}
        />
        <br />
        <input
          type="text"
          name="email_paired"
          placeholder="Email Paired"
          value={formData.email_paired}
          onChange={handleChange}
        />
        <br />
        <label>
          Resend
          <input
            type="checkbox"
            name="resend"
            checked={formData.resend}
            onChange={handleChange}
          />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default TestEmailForm;
