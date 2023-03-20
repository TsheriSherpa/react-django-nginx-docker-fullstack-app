import { Link } from "react-router-dom";
import MasterLayout from "./MasterLayout";
import { Modal, Button } from "react-bootstrap";

function ConsumerAppAdd() {
	return (
        <MasterLayout navbarTitle={"Consumer Apps"}>
            <div className="row m-auto">
                <div className="d-flex flex-row" style={{ margin: "30px" }}>
                    {/* <button type="button" class="btn btn-info">
                        <Link id="sample_editable_1_new" className="btn add-btn"
                            to="https://mnmdev1.truestreamz.com/admin/audios/create">
                            <i className="fa fa-plus"/>Add New
                        </Link>
                    </button> */}
                    <Button variant="info">Close</Button>
                </div>
                <div className="col-md-12">
                    <div className="table-responsive">
                        <table className="table table-bordered table-striped" id="table">
                            <thead className="thead-dark">
                                <tr>
                                    <th width="15%">Banner_title</th>
                                    <th width="15%">Image</th>
                                    <th width="15%">Type</th>
                                    <th width="10%">Status</th>
                                    <th width="10%">Home Banner</th>
                                    <th width="12%">Created_at</th>
                                    <th width="9%"> Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>TESt</td>
                                    <td>TESt</td>
                                    <td>TESt</td>
                                    <td>TESt</td>
                                    <td>TESt</td>
                                    <td>TESt</td>
                                    <td>TESt</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </MasterLayout>
	);
}
export default ConsumerAppAdd;
