import { useState } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'

function BookService() {
  const { serviceId } = useParams()
  const { state } = useLocation()
  const navigate = useNavigate()
  const serviceName = state?.serviceName || 'Service'

  const [form, setForm] = useState({
    customer_name: '',
    phone_number: '',
    address: '',
    preferred_time: ''
  })
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async () => {
    setLoading(true)
    const res = await fetch('http://34.234.44.64/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, service_id: parseInt(serviceId) })
    })
    if (res.ok) {
      setSuccess(true)
      setTimeout(() => navigate('/bookings'), 2000)
    }
    setLoading(false)
  }

  if (success) return (
    <div style={{ backgroundColor: '#0f0f1a', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ color: '#4caf50', fontSize: '1.5rem', textAlign: 'center' }}>
        ✅ Booking confirmed! Redirecting...
      </div>
    </div>
  )

  return (
    <div style={{ backgroundColor: '#0f0f1a', minHeight: '100vh', padding: '2rem', display: 'flex', justifyContent: 'center' }}>
      <div style={{ backgroundColor: '#1a1a2e', padding: '2rem', borderRadius: '12px', width: '100%', maxWidth: '500px', height: 'fit-content' }}>
        <h2 style={{ color: '#e94560', marginBottom: '1.5rem' }}>Book {serviceName}</h2>

        {['customer_name', 'phone_number', 'address', 'preferred_time'].map(field => (
          <div key={field} style={{ marginBottom: '1rem' }}>
            <label style={{ color: '#aaaaaa', display: 'block', marginBottom: '0.5rem' }}>
              {field.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </label>
            <input
              name={field}
              value={form[field]}
              onChange={handleChange}
              placeholder={field === 'preferred_time' ? 'e.g. 10am, Evening, 2pm' : ''}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid #e94560',
                backgroundColor: '#0f0f1a',
                color: '#ffffff',
                fontSize: '1rem',
                boxSizing: 'border-box'
              }}
            />
          </div>
        ))}

        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            width: '100%',
            padding: '1rem',
            backgroundColor: '#e94560',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1.1rem',
            fontWeight: 'bold',
            cursor: 'pointer',
            marginTop: '1rem'
          }}
        >
          {loading ? 'Booking...' : 'Confirm Booking'}
        </button>
      </div>
    </div>
  )
}

export default BookService
