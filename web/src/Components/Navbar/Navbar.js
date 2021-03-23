import {Button,Layout, Menu, Avatar} from "antd";
import ButtonGroup from "antd/lib/button/button-group";
import React from "react";
import { useAuth0 } from "@auth0/auth0-react";


function Navbar() {
  const { logout } = useAuth0();


  return (
    <Layout.Header>
      <div className="logo"></div>
      <Menu theme="dark" mode="horizontal">
        <Menu.Item key="1">Train</Menu.Item>
        <Menu.Item key="2">Test</Menu.Item>
        <Menu.Item key="3">Inference</Menu.Item>
        {/*
        <Avatar>
            R
        </Avatar>*/}
        <Button type='danger' style ={{float:'right'}} onClick = {() => logout({  returnTo: 'http://localhost:3000/' })}>
        Logout
      </Button>

      </Menu>
      
    </Layout.Header>
  );
}

export default Navbar;
