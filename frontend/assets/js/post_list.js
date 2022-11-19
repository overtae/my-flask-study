// API 기본 URL들을 정의합니다.
const postListBseUrl = 'http://127.0.0.1:5000/posts/';
const imageRetrieveBseUrl = 'http://127.0.0.1:5000/statics/';

/** Flask API 로부터 데이터를 가져옵니다.
 * promise 객체를 반환합니다.
 */
async function getPostListDatafromAPI(page = 1) {
  try {
    const somePromise = await fetch(postListBseUrl + '?page=' + page);
    const result = somePromise.json();
    return result;
  } catch (error) {
    console.log(error);
  }
}

/**
 * post Div 전체를 복사해 반환합니다.
 */
function getCopyDiv() {
  const postDiv = document.querySelector('.post');
  const newNode = postDiv.cloneNode(true);
  newNode.id = 'copied-post';
  newNode.style = 'display=inline';
  return newNode;
}

/**
 * id, 제목, 내용, 저자, 사진을 받아 해당 div를 하나의 게시물로 완성합니다.
 */
function getCompletedPost(
  idValue,
  titleValue,
  contentValue,
  authorNameValue,
  feedImgValue
) {
  div = getCopyDiv();
  let authorUpImg = div.children[0].children[0].children[0];
  let authorUpName = div.children[0].children[0].children[1];
  let feedImg = div.children[1];
  let authorDownName = div.children[2].children[3];
  let title = div.children[2].children[4];
  let content = div.children[2].children[5];
  let postTime = div.children[2].children[6];

  div.id = idValue;
  title.innerText = titleValue;
  content.innerText = contentValue;
  authorUpName.innerText = authorNameValue;
  authorDownName.innerText = authorNameValue;
  feedImg.src = feedImgValue;

  return div;
}

/**
 * 게시물 데이터를 받아온 다음,
 * 일정한 조건이 되면 호출되는 메서드입니다.
 * 페이지를 받아서, 적절한 데이터를 받아 화면에 그립니다.
 */
function loadMorePosts(page) {
  getPostListDatafromAPI(page).then((result) => {
    const postDiv = document.querySelector('.post-wrapper');
    for (let i = 0; i < result.length; i++) {
      const id = result[i]['id'];
      const title = result[i]['title'];
      const content = result[i]['content'];
      const author = result[i]['author_name'];
      const image = imageRetrieveBseUrl + result[i]['image'];

      postDiv.append(
        getCompletedPost(
          (idValue = id),
          (titleValue = title),
          (contentValue = content),
          (authorNameValue = author),
          (feedImgValue = image)
        )
      );
    }
  });
}

/**
 * 무한 스크롤
 */
function executeInfiniteScroll() {
  let pageCount = 1;
  var intersectionObserver = new IntersectionObserver(function (entries) {
    if (entries[0].intersectionRatio <= 0) {
      return;
    }

    loadMorePosts(pageCount);
    pageCount++;
  });
  intersectionObserver.observe(document.querySelector('.bottom'));
}

function main() {
  executeInfiniteScroll(); // 스크롤을 내릴 때마다 게시물 로드
}

main();
