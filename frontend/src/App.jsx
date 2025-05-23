import { Route, Routes, BrowserRouter } from "react-router-dom";
import { useState, useEffect } from "react";
import MainWrapper from "./layouts/MainWrapper";
import PrivateRoute from "./layouts/PrivateRoute";

import { CartContext, ProfileContext } from "./views/plugin/Context";

import Search from "./views/base/Search";

import Register from "../src/views/auth/Register";
import StudentDashbord from "views/student/Dashbord";

import StudentCourse from "viws/student/Courses";
import Courses from "viws/student/Courses";
import StudentCourseDetail from "./views/student/CourseDetail";

import CourseDetail from "./views/base/CourseDetail";
import Wishlist from "./views/student/Wishlist";
import StudentProfile from "./views/student/Profile";
import useAxios from "./utils/useAxios";
import UserData from "./views/plugin/UserData";
import StudentChangePassword from "./views/student/ChangePassword";

import Login from "../src/views/auth/Login";
import Logout from "./views/auth/Logout";
import ForgotPassword from "./views/auth/ForgotPassword";
import CreateNewPassword from "./views/auth/CreateNewPassword";
import Index from "./views/base/Index";
import Cart from "./views/base/Cart";
import Checkout from "./views/base/Cart";
import apiInstance from "./utils/axios";

import CartId from "./views/plugin/CartId";

function App() {
  const [cartCount, setCartCount] = useState(0);
  const [profile, setProfile] = useState({
    image: "",
    full_name: "",
    about: "",
    country: "",
  });

  useEffect(() => {
    apiInstance.get(`course/cart-list/${CartId()}/`).then((res) => {
      setCartCount(res.data?.length);
    });

    //console.log("cartCount", cartCount);

    useAxios()
      .get(`user/profile/${UserData()?.user_id}/`)
      .then((res) => {
        setProfile(res.data);
      });
  }, []);

  return (
    <BrowserRouter>
      <ProfileContext.Provider
        value={[profile, setProfile]}
      ></ProfileContext.Provider>
      <MainWrapper>
        <Routes>
          <Route path="/register/" element={<Register />} />
          <Route path="/login/" element={<Login />} />
          <Route path="/logout/" element={<Logout />} />
          <Route path="/forgot-password/" element={<ForgotPassword />} />
          <Route path="/create-new-password/" element={<CreateNewPassword />} />
          {/*BASE ROUTES */}
          <Route path="/" element={<Index />} />
          <Route path="/course-detail/:slug" element={<CourseDetail />} />
          <Route path="/cart/" element={<Cart />} />
          <Route path="/checkout/:order_oid/" element={<Checkout />} />
          <Route path="/search/" element={<Search />} />

          {/*student routes*/}
          <Route path="/student/dashboard/" element={<StudentDashbord />} />
          <Route path="/student/courses/" element={<Courses />} />
          <Route
            path="/student/courses/:enrollment_id"
            element={<StudentCourseDetail />}
          />
          <Route path="/student/wishlist/" element={<Wishlist />} />
          <Route path="/student/profile/" element={<StudentProfile />} />
          <Route
            path="/student/change-password/"
            element={<StudentChangePassword />}
          />
        </Routes>
      </MainWrapper>
    </BrowserRouter>
  );
}

export default App;
