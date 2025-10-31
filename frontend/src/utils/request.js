import axios from "axios";

axios.defaults.withCredentials = true
const request = 'http://127.0.0.1:1234/'
const request2=axios.create({
    baseURL: 'http://127.0.0.1:1234/',
}
)

const url = import.meta.env.VITE_API_URL
const request1=axios.create({
    baseURL: url ,
})
export {request,request1, request2} ;