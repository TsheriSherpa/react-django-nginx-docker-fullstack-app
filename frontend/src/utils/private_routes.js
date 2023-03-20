import { useSelector } from 'react-redux'
import { Outlet, Navigate } from 'react-router-dom'

// Private use for protecting authenticated routes
const PrivateRoutes = () => {
    let auth = useSelector((state) => state.user.loggedIn)

    return (
        auth ? <Outlet/> : <Navigate  to='/login'/>
    )
}

export default PrivateRoutes