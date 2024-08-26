import { useState } from 'react'
import {Link, useNavigate} from 'react-router-dom'
import styled from 'styled-components'
import { GiHamburgerMenu } from 'react-icons/gi'
import toast from "react-hot-toast"

function Header({ currentUser, updateUser }) {
 const [menu, setMenu] = useState(false)
 const navigate = useNavigate()

  const handleDelete = () => {
    fetch("/signout", {method: "DELETE"})
    .then(resp => {
      if (resp.ok) {
        updateUser(null)
        toast.success("See you soon!")
        navigate("/")

      } else {
        resp.json().then(errorObj => toast.error(errorObj.error))
      }
    })
  }
    return (
        <Nav> 
         <NavH1>Flatiron Theater Company</NavH1>
         <Menu>
           {!menu?
           <div onClick={() => setMenu(!menu)}>
             <GiHamburgerMenu size={30}/> 
           </div>:
           <ul>
            <li onClick={() => setMenu(!menu)}>x</li>
            <li><Link to='/'> Home</Link></li>
            {currentUser && (
              <>
                <li ><Link to='/productions/new'>New Production</Link></li>
                  <button onClick={handleDelete}>Logout</button>
              </>
            )}
            {!currentUser && <li><Link to='/registration'> Registration</Link></li>}
           </ul>
           }
         </Menu>

        </Nav>
    )
}

export default Header


const NavH1 = styled.h1`
font-family: 'Splash', cursive;
`
const Nav = styled.div`
  display: flex;
  justify-content:space-between;
  
`;

const Menu = styled.div`
  display: flex;
  align-items: center;
  a{
    text-decoration: none;
    color:white;
    font-family:Arial;
  }
  a:hover{
    color:pink
  }
  ul{
    list-style:none;
  }
  
`;