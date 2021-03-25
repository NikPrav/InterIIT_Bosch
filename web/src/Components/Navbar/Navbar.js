import {Layout, Menu, Avatar, Button, Steps, Image} from "antd";
import React from "react";
import {useAuth0} from "@auth0/auth0-react";
import {Link} from "react-router-dom";

function Navbar(props) {
  const {Step} = Steps;
  const {activePage, isOutside, workspace} = props;
  const {user, isAuthenticated, logout} = useAuth0();
  return (
    <Layout.Header>
      <div className="logo"></div>
      <Menu theme="dark" mode="horizontal" selectedKeys={activePage}>
        {!isOutside && (
          <Menu.Item key="1" onClick="/editor">
            <a href="/editor">Dataset</a>
          </Menu.Item>
        )}
        {!isOutside && (
          <Menu.Item key="2" onClick="/trainer">
            <Link href={`/trainer?workspace_id=${workspace}`}>Trainer</Link>
          </Menu.Item>
        )}
        {!isOutside && (
          <Menu.Item key="3" onClick="/trainer">
            <Link href={`/infer?workspace_id=${workspace}`}>Inference</Link>
          </Menu.Item>
        )}

        {isAuthenticated && (
          <Avatar
            src={user.picture}
            style={{float: "right", marginTop: "15px", marginLeft: "25px"}}
          />
        )}
        <Button
          type="danger"
          style={{float: "right", paddingLeft: "10px", marginTop: "15px"}}
          onClick={() => logout({returnTo: window.location.origin})}
        >
          Sign out
        </Button>
        {activePage == 1 && (
          <Button
            type="primary"
            href="/trainer"
            style={{float: "right", paddingLeft: "10px", marginTop: "15px", marginRight: "10px"}}
          >
            <Link href={`/editor?workspace_id=${workspace}`}>Proceed</Link>
          </Button>
        )}
      </Menu>
    </Layout.Header>
  );
}

export default Navbar;
