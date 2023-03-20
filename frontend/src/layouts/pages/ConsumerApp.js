import { useMemo, useState, useEffect} from "react";
import MasterLayout from "./MasterLayout";
import { Modal, Button } from "react-bootstrap";
import AddAppModal from "../components/AddAppModal";
import DataTable from 'react-data-table-component';
import FilterComponent from "../components/FilterComponent";

const columns = [
    {
        name: 'id',
        selector: row => row.id,
        // width: '100px'
    },
    {
        name: 'coverimage',
        cell: row => <img src={row.coverimage} width={50} alt={row.name}></img>,
        selector: row => row.coverimage,
        // width: '100px'
    },
    {
        name: 'name',
        selector: row => row.name,
        // width: '200px'
    },
    {
        name: 'detail',
        selector: row => row.detail,
        // width: '500px'
    },
    {
        name: 'latitude',
        selector: row => row.latitude,
        // width: '100px'
    },
    {
        name: 'longitude',
        selector: row => row.longitude,
        // width: '100px'
    },
];
  
function ConsumerApp() {
    const [modalOpen, setToggleModal] = useState(false);
    const [filterText, setFilterText] = useState('');
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [items, setItems] = useState([123]);
    const [totalRows, setTotalRows] = useState(0);
    const [perPage, setPerPage] = useState(10);
    const [resetPaginationToggle, setResetPaginationToggle] = useState(false);

    useEffect(() => {
        fetchData(1, perPage);
    }, [perPage])

    const fetchData = async (page, per_page) => {
       await fetch(`https://www.mecallapi.com/api/attractions?page=${page}&per_page=${per_page}`)
            .then(res => res.json())
            .then(
                (result) => {
                    setIsLoaded(true);
                    setItems(result.data);
                    setTotalRows(result.total);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }

    const handlePageChange = page => {
        fetchData(page, perPage);
    }

    const handlePerRowsChange = async (newPerPage, page) => {
        setPerPage(newPerPage);
    }

    const filteredItems = items.filter(
        item =>
            item.name && item.name.toLowerCase().includes(filterText.toLowerCase())
    )

    const subHeaderComponentMemo = useMemo(() => {
		const handleClear = () => {
			if (filterText) {
				setResetPaginationToggle(!resetPaginationToggle);
				setFilterText('');
			}
        }

        return (
            <FilterComponent
                onFilter={(e) => setFilterText(e.target.value)}
                onClear={handleClear}
                filterText={filterText} />
        );
    }, [filterText, resetPaginationToggle]);


    if (error) {
        return <div>Error: {error.message}</div>;
    } else {
        return (
            <MasterLayout navbarTitle={"Consumer Apps"}>
                <div className="col-md-12" >
                    <div className="d-flex flex-row" style={{ margin: "30px", marginLeft: "4px" }}>
                        <Button variant="info" onClick={() => setToggleModal(!modalOpen)}>Add App</Button>
                    </div>
                    <div  >
                        <h3 style={{ float: "left", paddingLeft: "10px" }}>Apps</h3>
                        <DataTable
                            progressPending={!isLoaded}
                            columns={columns}
                            data={filteredItems}
                            subHeader
			                subHeaderComponent={subHeaderComponentMemo}
                            pagination
                            paginationServer
                            paginationTotalRows={totalRows}
                            paginationResetDefaultPage={resetPaginationToggle}
                            onChangePage={handlePageChange}
                            onChangeRowsPerPage={handlePerRowsChange}
                        />
                    </div>
                    <AddAppModal modalOpen={modalOpen} setToggleModal={setToggleModal} />
                </div>
            </MasterLayout>
        );
    }

}
export default ConsumerApp;
