// Wholesale2Flip Discord Bot
// File: bot/index.js

const { Client, GatewayIntentBits, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle, SlashCommandBuilder } = require('discord.js');
const axios = require('axios');
require('dotenv').config();

class Wholesale2FlipBot {
    constructor() {
        this.client = new Client({
            intents: [
                GatewayIntentBits.Guilds,
                GatewayIntentBits.GuildMessages,
                GatewayIntentBits.MessageContent,
                GatewayIntentBits.GuildMembers
            ]
        });

        this.apiBaseUrl = process.env.API_BASE_URL || 'https://api.wholesale2flip.com/v1';
        this.apiKey = process.env.API_KEY;
        
        this.setupEventHandlers();
        this.setupCommands();
    }

    setupEventHandlers() {
        this.client.once('ready', () => {
            console.log(`✅ Wholesale2Flip Bot is online! Logged in as ${this.client.user.tag}`);
            this.client.user.setActivity('Real Estate Deals', { type: 'WATCHING' });
            this.registerSlashCommands();
        });

        this.client.on('interactionCreate', async (interaction) => {
            if (interaction.isChatInputCommand()) {
                await this.handleSlashCommand(interaction);
            } else if (interaction.isButton()) {
                await this.handleButtonInteraction(interaction);
            }
        });

        this.client.on('guildMemberAdd', async (member) => {
            await this.welcomeNewMember(member);
        });
    }

    setupCommands() {
        this.commands = new Map([
            ['deals', this.showDeals.bind(this)],
            ['search', this.searchProperties.bind(this)],
            ['profile', this.showProfile.bind(this)],
            ['alerts', this.manageAlerts.bind(this)],
            ['analyze', this.analyzeDeal.bind(this)],
            ['market', this.marketStats.bind(this)],
            ['help', this.showHelp.bind(this)]
        ]);
    }

    async registerSlashCommands() {
        const commands = [
            new SlashCommandBuilder()
                .setName('deals')
                .setDescription('View available real estate deals')
                .addStringOption(option =>
                    option.setName('market')
                        .setDescription('Market/city to search in')
                        .setRequired(false)
                )
                .addIntegerOption(option =>
                    option.setName('max_price')
                        .setDescription('Maximum price filter')
                        .setRequired(false)
                ),

            new SlashCommandBuilder()
                .setName('search')
                .setDescription('Search for specific properties')
                .addStringOption(option =>
                    option.setName('criteria')
                        .setDescription('Search criteria (e.g., "3BR Atlanta under 150k")')
                        .setRequired(true)
                ),

            new SlashCommandBuilder()
                .setName('profile')
                .setDescription('View or update your investor profile'),

            new SlashCommandBuilder()
                .setName('alerts')
                .setDescription('Manage your deal alerts')
                .addStringOption(option =>
                    option.setName('action')
                        .setDescription('Action to perform')
                        .setRequired(true)
                        .addChoices(
                            { name: 'View Active', value: 'view' },
                            { name: 'Create New', value: 'create' },
                            { name: 'Pause All', value: 'pause' }
                        )
                ),

            new SlashCommandBuilder()
                .setName('analyze')
                .setDescription('Analyze a real estate deal')
                .addIntegerOption(option =>
                    option.setName('purchase_price')
                        .setDescription('Purchase price')
                        .setRequired(true)
                )
                .addIntegerOption(option =>
                    option.setName('arv')
                        .setDescription('After Repair Value')
                        .setRequired(true)
                )
                .addIntegerOption(option =>
                    option.setName('repairs')
                        .setDescription('Estimated repair costs')
                        .setRequired(false)
                ),

            new SlashCommandBuilder()
                .setName('market')
                .setDescription('Get market statistics')
                .addStringOption(option =>
                    option.setName('location')
                        .setDescription('Market/city name')
                        .setRequired(true)
                ),

            new SlashCommandBuilder()
                .setName('help')
                .setDescription('Show available commands and features')
        ];

        try {
            await this.client.application.commands.set(commands);
            console.log('✅ Slash commands registered successfully');
        } catch (error) {
            console.error('❌ Error registering slash commands:', error);
        }
    }

    async handleSlashCommand(interaction) {
        const command = this.commands.get(interaction.commandName);
        if (!command) return;

        try {
            await interaction.deferReply();
            await command(interaction);
        } catch (error) {
            console.error(`Error executing command ${interaction.commandName}:`, error);
            
            const errorEmbed = new EmbedBuilder()
                .setColor('#ef4444')
                .setTitle('❌ Command Error')
                .setDescription('Sorry, there was an error processing your request. Please try again later.')
                .setTimestamp();

            await interaction.editReply({ embeds: [errorEmbed] });
        }
    }

    async showDeals(interaction) {
        const market = interaction.options.getString('market');
        const maxPrice = interaction.options.getInteger('max_price');

        const deals = await this.fetchDeals({ market, maxPrice });

        if (!deals || deals.length === 0) {
            const embed = new EmbedBuilder()
                .setColor('#f59e0b')
                .setTitle('📭 No Deals Found')
                .setDescription('No deals match your criteria right now. Try adjusting your filters or check back later!')
                .setTimestamp();

            await interaction.editReply({ embeds: [embed] });
            return;
        }

        const embed = new EmbedBuilder()
            .setColor('#10b981')
            .setTitle('🏠 Available Real Estate Deals')
            .setDescription(`Found ${deals.length} deals${market ? ` in ${market}` : ''}`)
            .setTimestamp();

        deals.slice(0, 5).forEach((deal, index) => {
            const profitEmoji = deal.profit_potential > 30000 ? '🔥' : deal.profit_potential > 15000 ? '💰' : '💵';
            
            embed.addFields({
                name: `${profitEmoji} ${deal.address}`,
                value: `**Price:** $${deal.price.toLocaleString()}\n**ARV:** $${deal.arv.toLocaleString()}\n**Profit:** $${deal.profit_potential.toLocaleString()}\n**ROI:** ${deal.roi_percentage}%`,
                inline: true
            });
        });

        const buttons = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId('view_all_deals')
                    .setLabel('View All Deals')
                    .setStyle(ButtonStyle.Primary)
                    .setEmoji('🔍'),
                new ButtonBuilder()
                    .setCustomId('set_alert')
                    .setLabel('Set Alert')
                    .setStyle(ButtonStyle.Secondary)
                    .setEmoji('🔔'),
                new ButtonBuilder()
                    .setURL(`${process.env.WEBSITE_URL}/deals`)
                    .setLabel('Open Dashboard')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('🌐')
            );

        await interaction.editReply({ embeds: [embed], components: [buttons] });
    }

    async searchProperties(interaction) {
        const criteria = interaction.options.getString('criteria');
        
        // Parse natural language search criteria
        const searchParams = this.parseSearchCriteria(criteria);
        const results = await this.fetchDeals(searchParams);

        const embed = new EmbedBuilder()
            .setColor('#3b82f6')
            .setTitle('🔍 Search Results')
            .setDescription(`Searching for: "${criteria}"\nFound ${results.length} matching properties`)
            .setTimestamp();

        if (results.length > 0) {
            results.slice(0, 3).forEach(property => {
                embed.addFields({
                    name: `${property.address}`,
                    value: `💰 $${property.price.toLocaleString()} | 🏆 $${property.profit_potential.toLocaleString()} profit\n📊 ${property.roi_percentage}% ROI | ${property.bedrooms}BR/${property.bathrooms}BA`,
                    inline: false
                });
            });
        } else {
            embed.setDescription('No properties found matching your search criteria. Try different keywords or broader criteria.');
        }

        await interaction.editReply({ embeds: [embed] });
    }

    async showProfile(interaction) {
        const user = await this.getDiscordUser(interaction.user.id);
        
        if (!user) {
            const embed = new EmbedBuilder()
                .setColor('#f59e0b')
                .setTitle('👤 Profile Not Found')
                .setDescription('You need to link your Wholesale2Flip account first!')
                .addFields({
                    name: '🔗 How to Link Your Account',
                    value: '1. Visit your dashboard\n2. Go to Account Settings\n3. Connect Discord\n4. Use code: `' + this.generateLinkCode() + '`'
                });

            const linkButton = new ActionRowBuilder()
                .addComponents(
                    new ButtonBuilder()
                        .setURL(`${process.env.WEBSITE_URL}/account/discord`)
                        .setLabel('Link Account')
                        .setStyle(ButtonStyle.Link)
                        .setEmoji('🔗')
                );

            await interaction.editReply({ embeds: [embed], components: [linkButton] });
            return;
        }

        const embed = new EmbedBuilder()
            .setColor('#1e3a8a')
            .setTitle(`👤 ${user.name}'s Profile`)
            .setThumbnail(interaction.user.displayAvatarURL())
            .addFields(
                { name: '📊 Subscription', value: user.subscription_tier, inline: true },
                { name: '🏠 Deals Closed', value: user.total_deals.toString(), inline: true },
                { name: '💰 Total Volume', value: `$${user.total_volume.toLocaleString()}`, inline: true },
                { name: '🎯 Target Markets', value: user.markets.join(', '), inline: true },
                { name: '💡 Investment Strategy', value: user.strategies.join(', '), inline: true },
                { name: '📈 Success Rate', value: `${user.success_rate}%`, inline: true }
            )
            .setTimestamp();

        const buttons = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId('update_profile')
                    .setLabel('Update Profile')
                    .setStyle(ButtonStyle.Secondary)
                    .setEmoji('✏️'),
                new ButtonBuilder()
                    .setURL(`${process.env.WEBSITE_URL}/dashboard`)
                    .setLabel('Open Dashboard')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('🌐')
            );

        await interaction.editReply({ embeds: [embed], components: [buttons] });
    }

    async analyzeDeal(interaction) {
        const purchasePrice = interaction.options.getInteger('purchase_price');
        const arv = interaction.options.getInteger('arv');
        const repairs = interaction.options.getInteger('repairs') || 0;

        const analysis = await this.performDealAnalysis({
            purchase_price: purchasePrice,
            arv: arv,
            repair_costs: repairs
        });

        const profitColor = analysis.net_profit > 20000 ? '#10b981' : 
                          analysis.net_profit > 10000 ? '#f59e0b' : '#ef4444';

        const recommendation = analysis.net_profit > 20000 ? '🟢 Excellent Deal!' :
                             analysis.net_profit > 10000 ? '🟡 Good Deal' :
                             analysis.net_profit > 0 ? '🟠 Marginal Deal' : '🔴 Avoid This Deal';

        const embed = new EmbedBuilder()
            .setColor(profitColor)
            .setTitle('📊 Deal Analysis Results')
            .setDescription(`**${recommendation}**`)
            .addFields(
                { name: '💰 Purchase Price', value: `$${purchasePrice.toLocaleString()}`, inline: true },
                { name: '🏆 ARV', value: `$${arv.toLocaleString()}`, inline: true },
                { name: '🔧 Repair Costs', value: `$${repairs.toLocaleString()}`, inline: true },
                { name: '📈 Gross Profit', value: `$${analysis.gross_profit.toLocaleString()}`, inline: true },
                { name: '💵 Net Profit', value: `$${analysis.net_profit.toLocaleString()}`, inline: true },
                { name: '📊 ROI', value: `${analysis.roi_percentage}%`, inline: true }
            )
            .addFields({
                name: '⚖️ Cost Breakdown',
                value: `Purchase: $${purchasePrice.toLocaleString()}\nRepairs: $${repairs.toLocaleString()}\nHolding: $${analysis.holding_costs.toLocaleString()}\nClosing: $${analysis.closing_costs.toLocaleString()}\n**Total Investment: $${analysis.total_investment.toLocaleString()}**`
            });

        if (analysis.risk_factors && analysis.risk_factors.length > 0) {
            embed.addFields({
                name: '⚠️ Risk Factors',
                value: analysis.risk_factors.join('\n')
            });
        }

        await interaction.editReply({ embeds: [embed] });
    }

    async marketStats(interaction) {
        const location = interaction.options.getString('location');
        const stats = await this.fetchMarketStats(location);

        if (!stats) {
            const embed = new EmbedBuilder()
                .setColor('#ef4444')
                .setTitle('❌ Market Not Found')
                .setDescription(`Could not find market data for "${location}". Try a different city or market name.`);

            await interaction.editReply({ embeds: [embed] });
            return;
        }

        const trendEmoji = stats.growth_rate > 5 ? '📈' : stats.growth_rate > 0 ? '📊' : '📉';
        const activityLevel = stats.total_properties > 100 ? 'High' : 
                            stats.total_properties > 50 ? 'Medium' : 'Low';

        const embed = new EmbedBuilder()
            .setColor('#1e3a8a')
            .setTitle(`📈 ${stats.market_name} Market Statistics`)
            .setDescription(`Market activity level: **${activityLevel}**`)
            .addFields(
                { name: '🏠 Available Properties', value: stats.total_properties.toString(), inline: true },
                { name: '💰 Avg Price', value: `$${stats.avg_price.toLocaleString()}`, inline: true },
                { name: '🏆 Avg ARV', value: `$${stats.avg_arv.toLocaleString()}`, inline: true },
                { name: '📊 Avg Profit Margin', value: `${stats.avg_profit_margin}%`, inline: true },
                { name: '⏰ Avg Days on Market', value: `${stats.avg_days_on_market} days`, inline: true },
                { name: `${trendEmoji} Growth Rate`, value: `${stats.growth_rate}%`, inline: true }
            )
            .setTimestamp();

        if (stats.top_neighborhoods && stats.top_neighborhoods.length > 0) {
            const neighborhoods = stats.top_neighborhoods
                .slice(0, 3)
                .map(n => `${n.name} ($${n.avg_price.toLocaleString()})`)
                .join('\n');
            
            embed.addFields({
                name: '🏘️ Top Neighborhoods',
                value: neighborhoods
            });
        }

        await interaction.editReply({ embeds: [embed] });
    }

    async showHelp(interaction) {
        const embed = new EmbedBuilder()
            .setColor('#3b82f6')
            .setTitle('🤖 Wholesale2Flip Bot Commands')
            .setDescription('Here are all the available commands:')
            .addFields(
                { name: '🏠 `/deals [market] [max_price]`', value: 'View available real estate deals', inline: false },
                { name: '🔍 `/search <criteria>`', value: 'Search for specific properties', inline: false },
                { name: '👤 `/profile`', value: 'View your investor profile', inline: false },
                { name: '🔔 `/alerts <action>`', value: 'Manage your deal alerts', inline: false },
                { name: '📊 `/analyze <price> <arv> [repairs]`', value: 'Analyze a real estate deal', inline: false },
                { name: '📈 `/market <location>`', value: 'Get market statistics', inline: false },
                { name: '❓ `/help`', value: 'Show this help message', inline: false }
            )
            .addFields({
                name: '🌟 Additional Features',
                value: '• Automatic deal notifications\n• Real-time market updates\n• Community discussions\n• Expert advice and tips'
            })
            .setFooter({ text: 'Need more help? Contact support@wholesale2flip.com' });

        await interaction.editReply({ embeds: [embed] });
    }

    async handleButtonInteraction(interaction) {
        await interaction.deferReply({ ephemeral: true });

        switch (interaction.customId) {
            case 'view_all_deals':
                await this.showAllDeals(interaction);
                break;
            case 'set_alert':
                await this.showAlertSetup(interaction);
                break;
            case 'update_profile':
                await this.showProfileUpdate(interaction);
                break;
            default:
                await interaction.editReply({ content: 'Unknown button interaction.' });
        }
    }

    async welcomeNewMember(member) {
        const welcomeChannel = member.guild.channels.cache.find(
            channel => channel.name === 'welcome' || channel.name === 'general'
        );

        if (!welcomeChannel) return;

        const embed = new EmbedBuilder()
            .setColor('#10b981')
            .setTitle('🎉 Welcome to Wholesale2Flip!')
            .setDescription(`Welcome ${member.user}, you've just joined the most active real estate investment community!`)
            .addFields(
                { name: '🚀 Get Started', value: 'Use `/profile` to set up your investor profile', inline: true },
                { name: '🏠 Find Deals', value: 'Use `/deals` to see available properties', inline: true },
                { name: '❓ Need Help?', value: 'Use `/help` to see all commands', inline: true }
            )
            .setThumbnail(member.user.displayAvatarURL())
            .setTimestamp();

        const welcomeButtons = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setURL(`${process.env.WEBSITE_URL}/onboarding`)
                    .setLabel('Complete Setup')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('🎯'),
                new ButtonBuilder()
                    .setURL(`${process.env.DISCORD_RULES_URL}`)
                    .setLabel('Read Rules')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('📋')
            );

        await welcomeChannel.send({ 
            content: `Welcome ${member.user}!`, 
            embeds: [embed], 
            components: [welcomeButtons] 
        });
    }

    // API Integration Methods
    async fetchDeals(filters = {}) {
        try {
            const params = new URLSearchParams();
            if (filters.market) params.append('market', filters.market);
            if (filters.maxPrice) params.append('max_price', filters.maxPrice);
            
            const response = await axios.get(`${this.apiBaseUrl}/properties?${params}`, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });
            
            return response.data.properties;
        } catch (error) {
            console.error('Error fetching deals:', error);
            return [];
        }
    }

    async getDiscordUser(discordId) {
        try {
            const response = await axios.get(`${this.apiBaseUrl}/users/discord/${discordId}`, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });
            return response.data.user;
        } catch (error) {
            return null;
        }
    }

    async performDealAnalysis(dealData) {
        try {
            const response = await axios.post(`${this.apiBaseUrl}/analytics/deal-analysis`, dealData, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });
            return response.data.analysis;
        } catch (error) {
            console.error('Error analyzing deal:', error);
            return {
                gross_profit: dealData.arv - dealData.purchase_price - dealData.repair_costs,
                net_profit: dealData.arv - dealData.purchase_price - dealData.repair_costs - 8000,
                roi_percentage: 15,
                total_investment: dealData.purchase_price + dealData.repair_costs + 8000,
                holding_costs: 5000,
                closing_costs: 3000
            };
        }
    }

    async fetchMarketStats(market) {
        try {
            const response = await axios.get(`${this.apiBaseUrl}/analytics/market-report/${encodeURIComponent(market)}`, {
                headers: { 'Authorization': `Bearer ${this.apiKey}` }
            });
            return response.data.report;
        } catch (error) {
            console.error('Error fetching market stats:', error);
            return null;
        }
    }

    // Utility Methods
    parseSearchCriteria(criteria) {
        const filters = {};
        const lower = criteria.toLowerCase();
        
        // Extract bedroom count
        const bedroomMatch = lower.match(/(\d+)\s*br/);
        if (bedroomMatch) filters.bedrooms = parseInt(bedroomMatch[1]);
        
        // Extract price range
        const priceMatch = lower.match(/under\s*\$?(\d+)k?/);
        if (priceMatch) {
            const price = parseInt(priceMatch[1]);
            filters.max_price = price > 1000 ? price : price * 1000;
        }
        
        // Extract city/market
        const cities = ['atlanta', 'birmingham', 'nashville', 'memphis', 'charlotte', 'jacksonville'];
        for (const city of cities) {
            if (lower.includes(city)) {
                filters.market = city;
                break;
            }
        }
        
        return filters;
    }

    generateLinkCode() {
        return Math.random().toString(36).substring(2, 8).toUpperCase();
    }

    async sendDealNotification(deal, channelId) {
        const channel = this.client.channels.cache.get(channelId);
        if (!channel) return;

        const embed = new EmbedBuilder()
            .setColor('#10b981')
            .setTitle('🚨 NEW DEAL ALERT!')
            .setDescription(`**${deal.address}**`)
            .addFields(
                { name: '💰 Price', value: `${deal.price.toLocaleString()}`, inline: true },
                { name: '🏆 ARV', value: `${deal.arv.toLocaleString()}`, inline: true },
                { name: '💵 Profit', value: `${deal.profit_potential.toLocaleString()}`, inline: true }
            )
            .setTimestamp();

        const buttons = new ActionRowBuilder()
            .addComponents(
                new ButtonBuilder()
                    .setURL(`${process.env.WEBSITE_URL}/properties/${deal.id}`)
                    .setLabel('View Details')
                    .setStyle(ButtonStyle.Link)
                    .setEmoji('🔍'),
                new ButtonBuilder()
                    .setCustomId(`express_interest_${deal.id}`)
                    .setLabel('Express Interest')
                    .setStyle(ButtonStyle.Primary)
                    .setEmoji('💰')
            );

        await channel.send({ embeds: [embed], components: [buttons] });
    }

    start() {
        this.client.login(process.env.DISCORD_BOT_TOKEN);
    }
}

// Export the bot class
module.exports = Wholesale2FlipBot;

// Start the bot if this file is run directly
if (require.main === module) {
    const bot = new Wholesale2FlipBot();
    bot.start();
}