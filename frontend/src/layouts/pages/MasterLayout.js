import AppNavbar from "../components/AppNavbar"
import Sidebar from "../components/Sidebar"

export default function MasterLayout ({ children }) {
    return (
        <div style={{ display: "block"}}>
            <AppNavbar></AppNavbar>
            <Sidebar></Sidebar>
            <div className="page-wrapper" id='page-wrapper'>
                <div className="content container-fluid">
                    {children}
                </div>
             </div>
         </div>
    )
};