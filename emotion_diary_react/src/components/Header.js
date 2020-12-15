import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useHistory } from 'react-router-dom';
import styled from 'styled-components';
import { logout } from '../store';

const HeaderStyle = styled.div`
  display: grid;
  width: 100%;
  height: 90%;
  grid-template-columns: 100%;
  border: 2px solid #003458;
  text-align: left;
  border-radius: 10px;
  padding: 150px 10px 10px 10px;
  font-size: 20px;
  background-color: #eaeae3;
`;
const ImgStyle = styled.img`
  width: 100%;
`;
const TitleStyle = styled.div`
  width: 100%;
  text-align: center;
  font-size: 30px;
`;
const UserBoxStyle = styled.div`
  display: grid;
  grid-template-columns: auto;
  justify-content: right;
`;
const ButtonStyle = styled.button`
  background-color: transparent;
  font-family: 'TDTDTadakTadak';
  font-size: ${(props) => (props.user ? '15px' : '20px')};
  // border: transparent;
  outline: transparent;
  text-align: left;
`;
const GroupBoxStyle = styled.div`
  text-align: left;
`;
const GroupStyle = styled.div`
  display: grid;
  grid-template-columns: 70% 30%;
`;
const ButtonSpanStyle = styled.span``;
const Header = () => {
  const isLogin = useSelector((store) => store.isLogin);
  const user = localStorage.getItem('userName');
  const history = useHistory();
  const dispatch = useDispatch();

  const [groups, setGroups] = useState([]);
  useEffect(() => {
    fetch('http://10.100.102.31:8000/tmember/get', {
      method: 'GET',
      headers: {
        Authorization: localStorage.getItem('Authorization'),
      },
    })
      .then((res) => res.json())
      .then((res) => {
        setGroups(res);
      });
  }, []);

  //로그아웃
  function submitLogout() {
    localStorage.clear();
    dispatch(logout());
    console.log(isLogin);
  }
  function modify(tno) {
    window.location.replace('/diary/ourmodify/' + tno);
  }
  console.log(groups);

  function refreshPage(id) {
    window.location.replace('/diary/our/' + id);
  }
  return (
    <HeaderStyle>
      <ImgStyle alt="" src="/images/logo.png" />
      <TitleStyle>{user}님</TitleStyle>
      <UserBoxStyle>
        <Link to={'/diary/usermodify/' + user}>
          <ButtonStyle user>회원 정보 수정</ButtonStyle>
        </Link>
        <Link to="/login">
          <ButtonStyle user onClick={submitLogout}>
            로그아웃
          </ButtonStyle>
        </Link>
      </UserBoxStyle>
      <Link to="/diary/">
        <ButtonStyle>나의 일기</ButtonStyle>
      </Link>
      <Link to="/diary/join">
        우리일기
        <ButtonStyle>
          <span class="badge badge-pill badge-success">만들기</span>
        </ButtonStyle>
      </Link>
      <GroupBoxStyle>
        {groups.map(({ tmno, member, together }) => (
          <GroupStyle key={tmno}>
            <ButtonStyle onClick={() => refreshPage(together.tno)}>
              {together.tname}
            </ButtonStyle>
            {/*    <button type="button" className="btn btn-warning btn-sm">
                수정
              </button> */}
            <span
              class="badge badge-pill badge-warning"
              onClick={() => modify(together.tno)}
            >
              수정
            </span>
          </GroupStyle>
        ))}
      </GroupBoxStyle>
      <div>내글 분석</div>
    </HeaderStyle>
  );
};

export default Header;
