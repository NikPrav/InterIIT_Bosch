import React, {useState, useEffect} from "react";
import {Layout, Typography, Image, Card} from "antd";
import Navbar from "../Navbar/Navbar";
import result from "./index_image.jpeg";
import {useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import request from "umi-request";

function Infer(props) {
  const {Title, Text, Link} = Typography;
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const [workspaceDetails, setWorkspaceDetails] = useState({});
  const workspace_id = parseInt(props.location.search.substr(14), 10);
  const getWorkSpaceDetails = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceReq = await request(
        `${process.env.REACT_APP_API_URL}/workspaces/${workspace_id}`,
        {
          method: "get",
          headers: {
            Authorization: `Bearer ${localaccessToken}`,
            email: `${user.email}`,
          },
        }
      );
      const umimessage = await userWorkSpaceReq;

      console.log(umimessage);
      setWorkspaceDetails(umimessage);
    } catch (e) {
      console.log(e.message);
    }
  };

  useEffect(
    async user => {
      console.log("Grab Workspace Details");
      await getWorkSpaceDetails();
    },
    [user]
  );
  return (
    <Layout>
      <Navbar activePage="3" workspace={workspace_id} />
      <Layout.Content style={{margin: "60px"}}>
        <Card style={{minHeight: "50vh"}}>
          <div>
            <Title>Criterion 1</Title>
            <div style={{display: "flex", justifyContent: "space-between", marginLeft: "5vw"}}>
              <Image src={result} width="30vw" />
              <Card style={{marginRight: "15vw"}} title="Saliency Map">
                This is a two-line description that will be provided by the backend
                <br />
                Second Line of Description
              </Card>
            </div>
          </div>
        </Card>
      </Layout.Content>
    </Layout>
  );
}

export default Infer;
