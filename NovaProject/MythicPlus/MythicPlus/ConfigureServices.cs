using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace MythicPlus
{
    public static class ConfigureServices
    {
        public static void AddMythicPlus(this IServiceCollection serviceCollection, IConfiguration config)
        {
            serviceCollection.AddEntityFrameworkNpgsql().AddDbContext<MythicPlusDbContext>(opt =>
                opt.UseNpgsql(config.GetConnectionString("database"))
            );
        }
    }
}