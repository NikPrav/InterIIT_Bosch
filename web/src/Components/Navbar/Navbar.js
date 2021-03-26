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
          <Menu.Item key="1" onClick={`/editor?workspace_id=${workspace}`}>
            <Link to={`/editor?workspace_id=${workspace}`}>Dataset</Link>
          </Menu.Item>
        )}
        {!isOutside && (
          <Menu.Item key="2">
            <Link to={`/trainer?workspace_id=${workspace}`}>Trainer</Link>
          </Menu.Item>
        )}
        {!isOutside && (
          <Menu.Item key="3">
            <Link to={`/infer?workspace_id=${workspace}`}>Inference</Link>
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
          <Link to={`/trainer?workspace_id=${workspace}`}>
            <Button
              type="primary"
              style={{float: "right", paddingLeft: "10px", marginTop: "15px", marginRight: "10px"}}
            >
              Proceed
            </Button>
          </Link>
        )}
      </Menu>
    </Layout.Header>
  );
}

export default Navbar;
