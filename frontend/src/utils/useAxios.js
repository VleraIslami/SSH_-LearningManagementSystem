// src/utils/useAxios.js
import axios from "axios";

const useAxios = () => {
    const apiInstance = axios.create({
        baseURL: "http://127.0.0.1:8000/api/v1/",
        headers: {
            'Content-Type': 'application/json',
        Accept: 'application/json',
        },
    });

    return apiInstance;
};

export default useAxios;
