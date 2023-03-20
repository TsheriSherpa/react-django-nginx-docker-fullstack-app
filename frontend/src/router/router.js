import Login from '../layouts/pages/Login';
import { Routes, Route} from 'react-router-dom'
import Dashboard from '../layouts/pages/Dashboard';
import PrivateRoutes from '../utils/private_routes';
import ConsumerApp from '../layouts/pages/ConsumerApp';


function AppRoutes() {	
	return (
		<Routes>
			<Route element={<PrivateRoutes />}>
				<Route path="/" element={<Dashboard/>} exact />
				<Route path="/consumer-apps" element={<ConsumerApp/>} exact />
			</Route>
			<Route path="/login" element={<Login />} />
			<Route path="*" element={<NoMatch />} />
		</Routes>
  	)
}

const NoMatch = () => {
	return <p style={{ marginTop: "300px", fontSize: "30px", color: "red" }}>Not Found : 404!</p>;
};
  
export default AppRoutes