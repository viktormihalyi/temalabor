using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Nest;

namespace webscraper.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductController : ControllerBase
    {
        private readonly IElasticClient _elasticClient;
        public ProductController(IElasticClient elasticClient){
            _elasticClient = elasticClient;
        }
        // GET api/values
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            
            return Ok("Teszt");
        }


        // GET api/product/name
        [HttpGet("search")]
        public async Task<IActionResult> Get(
            string category, 
            string title,
            int pageFrom = 0, 
            int pageTo = 1, 
            int pageSize = 20,
            int priceMin = -1,
            int priceMax = -1
        )
        {   
            
            QueryContainer qContainer = new QueryContainer();
            QueryContainerDescriptor<Product> qcd = new QueryContainerDescriptor<Product>();

            if(category != null)
            {
                qContainer = qContainer && qcd.Match(m => m
                        .Field(f => f.Category)
                        .Query(category)
                );
            }
            if (title != null)
            {
                qContainer = qContainer && qcd.MultiMatch(
                    s => s
                    .Fields(fs => fs
                        .Field(f=>f.Title)
                        .Field(f=>f.Description)
                    )
                    .Query(title)
                );
            }
            
            if(priceMin != -1){
                qContainer = qContainer && qcd.Range( m => m
                    .Field(f => f.Price)
                    .GreaterThanOrEquals(priceMin)
                );
            }

            if(priceMax != -1){
                qContainer = qContainer && qcd.Range(m => m
                  .Field(f=>f.Price)
                  .LessThanOrEquals(priceMax)
               );
            }
           
            var response = await _elasticClient.SearchAsync<Product>(s => s 
                .Query(_ => qContainer)
                .From(pageFrom*pageSize)
                .Size((pageTo-pageFrom)*pageSize)
            );

            var products = response.Documents;

            return Ok(products);
        }

       
    }
}
