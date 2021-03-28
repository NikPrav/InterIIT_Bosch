import React, {useState, useEffect} from "react";
import {Layout, Typography, Image, Card, Upload, Button} from "antd";
import Navbar from "../Navbar/Navbar";
import result from "./index_image.jpeg";
import {useParams} from "react-router";
import {useAuth0} from "@auth0/auth0-react";
import request from "umi-request";
import {FaUpload} from "react-icons/fa";

function Infer(props) {
  const {Title, Text, Link} = Typography;
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const [workspaceDetails, setWorkspaceDetails] = useState({});
  const workspace_id = parseInt(props.location.search.substr(14), 10);
  const [startInfer, setStartInfer] = useState(false);
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

  const handleOnChange = ({file, fileList, event}) => {
    console.log(file, fileList, event);
    //Using Hooks to update the state to the current filelist
    // setDefaultFileList(fileList);
    //filelist - [{uid: "-1",url:'Some url to image'}]
  };
  const toBase64 = file =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });

  const uploadImage = async options => {
    const {onSuccess, onError, file, onProgress} = options;
    console.log(`X:${file}`);
    console.log(file);
    try {
      const base64data = await toBase64(file);

      console.log(base64data);
      // console.log(atob(base64data))/

      const UrlToSendDataTo = `http://localhost:5000/${workspace_id}/rpc/infer`;
      const response = await request(UrlToSendDataTo, {
        method: "post",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({image: base64data}),
      });
      const res = response;
      onSuccess(file);
      console.log(`response:${res}`);
      console.log(res);
    } catch (e) {
      console.log(`Error:${e.message}`);
    }
  };
  return (
    <Layout>
      <Navbar activePage="3" workspace={workspace_id} />
      <Layout.Content style={{marginLeft: "60px", marginRight: "60px"}}>
        <Card style={{minHeight: "50vh"}}>
          <div>
            <p>
              Choose an image to start training!
              <br />
              <Upload
                customRequest={uploadImage}
                onChange={handleOnChange}
                style={{float: "right", marginLeft: "40px"}}
              >
                <Button icon={<FaUpload />} style={{float: "right"}}>
                  {" "}
                  Click to Upload
                </Button>
              </Upload>
            </p>
          </div>
          <div style={{paddingTop: "30px"}}>
            <Title style={{marginLeft: "2vw", fontSize: "30px"}}>SHAP Gradients</Title>
            <div style={{display: "flex", justifyContent: "space-between", marginLeft: "5vw"}}>
              <Image
                src="https://media.discordapp.net/attachments/817818352130195476/825096438190571550/shap.png"
                width="30vw"
                style={{minWidth: "30vw"}}
              />
              <Card style={{marginRight: "15vw", marginLeft: "15vw"}} title="SHAP Gradients">
                <br />
                This is a method to interpret the model predictions on a given image from the <br />
                perspective of optimal credit allocation with local. Explanations using the classic
                Shapley values from game theory and their related extensions.
              </Card>
            </div>

            <Title style={{paddingTop: "30px", fontSize: "30px", marginLeft: "2vw"}}>
              DeepLift
            </Title>
            <div style={{display: "flex", justifyContent: "space-between", marginLeft: "5vw"}}>
              <Image
                src="https://media.discordapp.net/attachments/817818352130195476/825096434273615962/deepl.png"
                width="30vw"
                style={{minWidth: "30vw"}}
              />
              <Card style={{marginRight: "15vw", marginLeft: "15vw"}} title="Deep Lift">
                DeepLIFT seeks to explain the difference in the output from reference in terms of
                the difference in inputs from <br />
                reference.DeepLIFT uses the concept of multipliers to "blame" specific neurons for
                the difference in output.
                <br />
                By allowing us to give separate consideration to positive and negative
                contributions, DeepLIFT can also reveal dependencies which are missed by other
                approaches
              </Card>
            </div>

            <Title style={{paddingTop: "30px", fontSize: "30px"}}>Criterion 1</Title>
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
