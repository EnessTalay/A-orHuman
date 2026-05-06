using Xunit;
using Moq;
using Moq.Protected;
using Microsoft.AspNetCore.Mvc;
using aıorhumanv2.Controllers;
using aıorhumanv2.Models;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;
using System.Text;
using System.Net;

namespace aıorhumanv2.Tests
{
    public class HomeControllerTestleri
    {
        [Fact]
        public void Index_Get_ModelIleViewDondurur()
        {
            // Arrange
            var mockFactory = new Mock<IHttpClientFactory>();
            var controller = new HomeController(mockFactory.Object);

            // Act
            var result = controller.Index();

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            Assert.IsType<TahminViewModel>(viewResult.Model);
        }

        [Fact]
        public async Task Index_Post_MetinBos_Ise_HataIleViewDondurur()
        {
            // Arrange
            var mockFactory = new Mock<IHttpClientFactory>();
            var controller = new HomeController(mockFactory.Object);
            var model = new TahminViewModel { Metin = "" };

            // Act
            var result = await controller.Index(model);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            var returnedModel = Assert.IsType<TahminViewModel>(viewResult.Model);
            Assert.NotNull(returnedModel.HataMesaji);
            Assert.Equal("Lütfen bir metin girin.", returnedModel.HataMesaji);
        }

        [Fact]
        public async Task Index_Post_Basarili_Ise_SonucIleViewDondurur()
        {
            // Arrange
            var mockFactory = new Mock<IHttpClientFactory>();
            var mockHttpMessageHandler = new Mock<HttpMessageHandler>();
            
            // Mock API response
            var apiResponse = new
            {
                final_prediction = "Human",
                final_ai_percent = 10,
                models = new 
                {
                    lr = new { ai_percent = 5 },
                    svm = new { ai_percent = 15 },
                    nb = new { ai_percent = 10 }
                }
            };
            var jsonResponse = JsonSerializer.Serialize(apiResponse);

            mockHttpMessageHandler.Protected()
                .Setup<Task<HttpResponseMessage>>(
                    "SendAsync",
                    ItExpr.IsAny<HttpRequestMessage>(),
                    ItExpr.IsAny<CancellationToken>()
                )
                .ReturnsAsync(new HttpResponseMessage
                {
                    StatusCode = HttpStatusCode.OK,
                    Content = new StringContent(jsonResponse)
                });

            var client = new HttpClient(mockHttpMessageHandler.Object);
            mockFactory.Setup(_ => _.CreateClient(It.IsAny<string>())).Returns(client);

            var controller = new HomeController(mockFactory.Object);
            var model = new TahminViewModel { Metin = "Test metni" };

            // Act
            var result = await controller.Index(model);

            // Assert
            var viewResult = Assert.IsType<ViewResult>(result);
            var returnedModel = Assert.IsType<TahminViewModel>(viewResult.Model);
            
            Assert.Equal("Human", returnedModel.FinalPrediction);
            Assert.Equal(10, returnedModel.FinalAiPercent);
            Assert.Equal(90, returnedModel.FinalHumanPercent); // 100 - 10
        }
    }
}
