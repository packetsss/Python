import axios from "axios";
import { useHistory } from "react-router-dom";

const facebookLogin = (response) => {
    console.log(response);
    axios
        .post("http://127.0.0.1:8000/auth/convert-token", {
            token: response.accessToken,
            username: response.name,
            email: response.email,
            backend: "facebook",
            grant_type: "convert_token",
            client_id: "uEB5hBk98NGoSgGinRqU8hsEsFC0uNlEVPAAMV9N",
            client_secret:
                "YvHpwCMcwe2m7dYj0Uf8AJMZfE5hqvV8DGPoJ2syweBpCac2KgzpaUq8rTChOpgsh7H75Z0fw6oMgdxhRe55f8FWadCRPcQqiCOEGASLTflk8zb7KEdh3SLoda1JeHpj",
            
        })
        .then((res) => {
            console.log(res.data);
            localStorage.setItem("access_token", res.data.access_token);
            localStorage.setItem("refresh_token", res.data.refresh_token);
            useHistory("/");
            window.location.reload();
        });
};

export default facebookLogin;
