import  {useParams, useNavigate } from 'react-router-dom'
import {useEffect, useState} from 'react'
import styled from 'styled-components'
import { useOutletContext } from 'react-router-dom'
import toast from "react-hot-toast"

function ProductionDetail() {
  const [production, setProduction] = useState(null)
  const [error, setError] = useState(null)
  const { handleEdit, deleteProduction, currentUser } = useOutletContext()

  //Student Challenge: GET One 
  const { projectId } = useParams()
  const navigate = useNavigate()

  useEffect(()=>{
    fetch(`/productions/${projectId}`)
      .then(resp => {
        if (resp.ok) {
          resp.json().then(setProduction)
        } else {
          resp.json().then(errorObj => toast.error(errorObj.error))
        }
      })
      .catch(errorObj => toast.error(errorObj.message))
  }, [projectId])

  const handleDelete = () => {
    fetch(`/productions/${projectId}`, {method: "DELETE"})
    .then(resp => {
      if (resp.status === 204) { 
        deleteProduction(production)
        navigate("/")
      } else {
        resp.json().then(errorObj => toast.error(errorObj.error))
      }
    })
    .catch(errorObj => toast.error(errorObj.message))
  }
  
  if(error) return <h2>{error}</h2>

  if (!production) return <h2>Loading...</h2>
  
  const {id, title, genre, image,description, crew_members} = production

  return (
      <CardDetail id={id}>
        <h1>{title}</h1>
          <div className='wrapper'>
            <div>
              <h3>Genre:</h3>
              <p>{genre}</p>
              <h3>Description:</h3>
              <p>{description}</p>
              <h2>Cast Members</h2>
              <ul>
                {crew_members.map(cast => <li key={cast.id}>{`${cast.role} : ${cast.name}`}</li>)}
              </ul>
            </div>
            <img src={image} alt={title}/>
          </div>
      {
        currentUser && currentUser.id === production.user_id && <>
          <button onClick={()=> handleEdit(production)} >Edit Production</button>
          <button onClick={handleDelete} >Delete Production</button>
        </>
      }
      </CardDetail>
    )
  }
  
  export default ProductionDetail
  const CardDetail = styled.li`
    display:flex;
    flex-direction:column;
    justify-content:start;
    font-family:Arial, sans-serif;
    margin:5px;
    h1{
      font-size:60px;
      border-bottom:solid;
      border-color:#42ddf5;
    }
    .wrapper{
      display:flex;
      div{
        margin:10px;
      }
    }
    img{
      width: 300px;
    }
    button{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
    }
  `