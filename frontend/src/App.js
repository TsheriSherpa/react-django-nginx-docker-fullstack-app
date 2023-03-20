import React from 'react'
import './styles/App.css';
import 'bootstrap/dist/css/bootstrap.css';
import {BrowserRouter as Router} from "react-router-dom";
import AppRoutes from './router/router';


function App() {
	return (
	 	 <div className='App'>
			<Router>
				<AppRoutes/>
			</Router>
		</div>
  	);
}

export default App;
