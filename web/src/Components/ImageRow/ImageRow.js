import React, {useState, useEffect} from "react";
import {Card, Col, Row, Upload, Button} from "antd";
import PopupImage from "../PopupImage/PopupImage";
import img from "./../PopupImage/stop.png";
import {FaUpload} from "react-icons/fa";
import "./styles.css";
import {useAuth0} from "@auth0/auth0-react";
import request from "umi-request";

function ImageRow(props) {
  const {workspace_id, DataClass} = props;
  console.log(workspace_id);
  let ImagePaths = [img];
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const [filesList, setfilesList] = useState([{}]);
  const [accessToken, setaccessToken] = useState([{}]);
  const [imageb64Paths, setImageb64Paths] = useState([]);
  const onChange = newfileList => {
    /*
      setfilesList([...filesList,newfileList]);
    */
  };

  const getImageDetails = async id => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceReq = await request(
        `${process.env.REACT_APP_API_URL}/workspaces/${workspace_id}/images/${id}`,
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
      setImageb64Paths([...imageb64Paths, umimessage]);
    } catch (e) {
      console.log(e.message);
    }
  };

  ImagePaths.forEach(id => {
    getImageDetails(id);
  });

  console.log(filesList);
  return (
    <div className="class-carousel">
      <Row
        gutter={6}
        style={{
          height: "120px",
          width: "100%",
          whiteSpace: "nowrap",
          overflowX: "scroll",
          flexWrap: "nowrap",
        }}
      >
        <Col style={{height: "100px", minWidth: "90px"}}>
          <Card style={{height: 90}}>
            {DataClass}
            <br />
            <Upload>
              <Button>
                <FaUpload />
              </Button>
            </Upload>
          </Card>
        </Col>
        {imageb64Paths.map(x => {
          <Col style={{minWidth: "90px"}}>
            <PopupImage source={x} />
          </Col>;
        })}
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        {filesList.map(file => {
          <PopupImage source={file} />;
        })}
        <Col>
          <Card style={{height: 90}}>
            <Upload style={{height: 90}} accept=".jpg,.jpeg,.png,.webp" fileList={[]}>
              <Button>
                <FaUpload />
              </Button>
            </Upload>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default ImageRow;
