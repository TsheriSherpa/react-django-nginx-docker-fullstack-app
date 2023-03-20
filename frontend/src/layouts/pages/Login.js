import '../../styles/login.css';
import { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import { useSelector, useStore } from 'react-redux';
import { login } from "/src/redux/reducers/userReducer";
import { authService } from "../../services/auth-service";
import { error as failure, clear } from "/src/redux/reducers/alertReducer"
import { Button } from "react-bootstrap";
import { useForm } from 'react-hook-form';
import { FaRegEyeSlash, FaRegEye } from "react-icons/fa";


export default function Login() {
    const store = useStore();
    const navigate = useNavigate();
    const { register, handleSubmit, formState } = useForm();
    const error = useSelector((state) => state.alert.error)
    const { isSubmitting, errors } = formState;
    const [passwordShown, setPasswordShown] = useState(false);
    const [showPassword, setShowPassword] = useState(true);

    const togglePassword = () => {
        setPasswordShown(!passwordShown);
        setShowPassword(!showPassword);
    };

    useEffect(() => {
        // redirect to dashboard if already logged in
        if (store.getState().user.loggedIn) {
            navigate("/");
        }
    })

    const submitFormHandler = (data) => {
        return new Promise((resolve) => {
            authService.loginUser(data.email, data.password)
                .then(
                    user => {
                        store.dispatch(login(user));
                        store.dispatch(clear());
                        navigate('/');
                    },
                    error => {
                        store.dispatch(failure(error.toString()));
                        setTimeout(() => store.dispatch(clear()), 5000)
                        resolve();
                    }
            );
        })
    }

    
    return (
        <div className="login-page">
            <div className="form">
                <form className="login-form" onSubmit={handleSubmit(submitFormHandler)}>
                    <h2>SIGN IN </h2>
                    {error && 
                        <span style={{ color:"red" }}>{error}</span>}
                    {errors.Email &&
                        <span style={{ color: "red" }}>{errors.Email.message}</span>}
                    
                    <input
                        type="text"
                        placeholder="Email"
                        name="email"
                        required
                        {
                            ...register("email",
                                { required: true }
                            )
                        }
                    />
                    <input
                        id="pass"
                        type={passwordShown ? "text" : "password"}
                        placeholder="password"
                        name="password"
                        required
                        {
                            ...register("password", {})
                        } />
                    
                    <div className="show-password-div" onClick={togglePassword}>
                        { showPassword && <FaRegEyeSlash id="hide-icon" />}
                        { !showPassword && <FaRegEye id="show-icon" />}
                    </div>

                    <span id="vaild-pass"></span>
                    <Button
                        type="submit"
                        variant="primary"
                        disabled={isSubmitting}
                    >
                        {isSubmitting &&
                            (<span className="spinner-border spinner-border-sm mr-1"></span>)}
                        Login
                    </Button>
                </form>
            </div>
        </div>
    );
}