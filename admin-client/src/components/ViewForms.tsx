import { useEffect, useState } from 'react';
import axios from 'axios';
import { local_endpoints } from '../App';

interface FormViewProps {
  formId: number;
}

function FormView({ formId }: FormViewProps) {
  const [unpaired, setUnpaired] = useState<string[]>([]);
  const [paired, setPaired] = useState<[string, string][]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    // Fetch form data
    async function fetchFormData() {
      try {
        const unpairedResponse = await axios.get(`${local_endpoints.unpaired}/${formId}`);
        const pairedResponse = await axios.get(`${local_endpoints.paired}/${formId}`);
        setUnpaired(unpairedResponse.data.unpaired);
        setPaired(pairedResponse.data.pairs);
      } catch (error) {
        console.error('Error fetching form data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchFormData();
  }, [formId]); // Update useEffect dependency to formId

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Viewing Form {formId}</h2>
      <h3>Unpaired</h3>
      <ul>
        {unpaired.map((email, i) => (
          <li key={i}>{email}</li>
        ))}
      </ul>
      <h2>Paired</h2>
      <ul>
        {paired.map((pair, i) => (
          <li key={i}>
            {pair[0]} - {pair[1]}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function ViewForms() {
  const [formIds, setFormIds] = useState<number[]>([]);
  const [viewing, setViewing] = useState<number | null>(null);

  useEffect(() => {
    async function fetchFormData() {
      try {
        const response = await axios.get(local_endpoints.forms);
        setFormIds(response.data.forms);
      } catch (error) {
        console.error('Error fetching form data:', error);
      }
    }

    fetchFormData();
  }, []);

  const toggleView = (index: number) => {
    setViewing(prevViewing => prevViewing === index ? null : index);
  };

  return (
    <div>
      <h1>Forms</h1>
      {viewing !== null && <FormView formId={formIds[viewing]} />}
      <ul>
        {formIds.map((formId, i) => (
          <li key={i}>
            <button onClick={() => toggleView(i)}>{i === viewing ? "Hide" : "Show"} {formId}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
