import {Layout, Menu, Avatar, Button} from "antd";
import React from "react";

function Navbar() {
  return (
    <Layout.Header>
      <div className="logo"></div>
      <Menu theme="dark" mode="horizontal">
        <Menu.Item key="1">Train</Menu.Item>
        <Menu.Item key="2">Test</Menu.Item>
        <Menu.Item key="3">nav1</Menu.Item>
        {/*
        <Avatar>
            R
        </Avatar>
        <Button>
            Sign out
        </Button>
*/}
      </Menu>
    </Layout.Header>
  );
}

export default Navbar;
